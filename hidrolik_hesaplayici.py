# -*- coding: utf-8 -*-
"""
/***************************************************************************
 HidrolikHesaplayici
                                 A QGIS plugin
 Bu plugin bir kanal sistemi icin özel olarak yapilmis hidrolik hesaplamar yapmayı saglamaktadir. Proje yönetimini Eren Kücük, Oguzhan Alayont, Atalay Berk Cirak ve  Emre Erdogan gerçekleştirmiştir.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-12-24
        git sha              : $Format:%H$
        copyright            : (C) 2024 by EmirKivrak
        email                : emirkvrak.00@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsMapLayer

from qgis.core import QgsField, edit
from PyQt5.QtCore import QVariant

from qgis.core import QgsVectorLayer



import math

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .hidrolik_hesaplayici_dialog import HidrolikHesaplayiciDialog
import os.path


class HidrolikHesaplayici:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        
        self.dlg = HidrolikHesaplayiciDialog()
        
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'HidrolikHesaplayici_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Hidrolik Hesaplayici')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('HidrolikHesaplayici', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/hidrolik_hesaplayici/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Hidrolik Hesaplayici'),
            callback=self.run,
            parent=self.iface.mainWindow())

        
        
        self.dlg.CBLayer.layerChanged.connect(self.__attributeSutunGet)
        self.dlg.RBdem.toggled.connect(self.__radioButtonSelected)
        self.dlg.RBzemin.toggled.connect(self.__radioButtonSelected)
        
        self.dlg.PBalanHesap.clicked.connect(self.__alanHesapla)
        self.dlg.PBortaBolumHesap.clicked.connect(self.__ortaBolumHesaplamalari)
        self.dlg.PBkaziHacmiHesap.clicked.connect(self.__kaziHacmiHesaplama)
        
        self.dlg.PBtumunuHesapla.clicked.connect(self.__tumunuHesapla)
        
        # will be set False in run()
        self.first_start = True
    

    
        
    
    def __radioButtonSelected(self, checked):
        if self.dlg.RBdem.isChecked():
            print("Dem Dosyası seçildi!")
            self.dlg.CBDemLayer.setEnabled(True)
            self.dlg.CBzeminKotBas.setEnabled(False)
            self.dlg.CBzeminKotSon.setEnabled(False)
        elif self.dlg.RBzemin.isChecked():
            print("Zemenin Kot Sütunları seçildi!")
            self.dlg.CBDemLayer.setEnabled(False)
            self.dlg.CBzeminKotBas.setEnabled(True)
            self.dlg.CBzeminKotSon.setEnabled(True)
            
    def __tumunuHesapla(self):
        if not self.__alanHesapla():
            self.dlg.Tcikti.append("Hata: __alanHesapla başarısız.")
            return
        if not self.__ortaBolumHesaplamalari():
            self.dlg.Tcikti.append("Hata: __ortaBolumHesaplamalari başarısız.")
            return
        if not self.__kaziHacmiHesaplama():
            self.dlg.Tcikti.append("Hata: __kaziHacmiHesaplama başarısız.")
            return
        
                # Hata durumunda işlem durdurulur       
        self.dlg.Tcikti.append("Tüm işlemler başarıyla tamamlandı!")

        
        
    def __ortaBolumHesaplamalari(self):
        # Seçili katmanı al
        selected_layer = self.dlg.CBLayer.currentLayer()

        # Eğer hiçbir şey seçilmemişse, hata mesajını Tcikti'ye yazdır
        if selected_layer is None:
            self.dlg.Tcikti.append("Hata: Lütfen geçerli bir katman seçin!")
            return False

        # Eğer bir katman seçilmişse, seçilen katman adını Tcikti'ye yazdır
        self.dlg.Tcikti.append(f"Seçili Katman: {selected_layer.name()}")
        
        cbboruKotBaslangic = self.dlg.CBboruKotBaslangic.currentText()
        cbboruKotSon = self.dlg.CBboruKotSon.currentText()
        cbcap = self.dlg.CBcap.currentText()
        cbmanning = self.dlg.CBmanning.currentText()
        
        
        if not cbboruKotBaslangic or cbboruKotBaslangic == "Seçiniz":
            self.dlg.Tcikti.append("Hata: Lütfen (Boru Taban Kot Başlangıcı) Sütununu Seçiniz!")
            return False
        if not cbboruKotSon or cbboruKotSon == "Seçiniz":
            self.dlg.Tcikti.append("Hata: Lütfen (Boru Taban Kot Son) Sütununu Seçiniz!")
            return False
        if not cbcap or cbcap == "Seçiniz":
            self.dlg.Tcikti.append("Hata: Lütfen (Çap (mm)) Sütununu Seçiniz!")
            return False
        if not cbmanning or cbmanning == "Seçiniz":
            self.dlg.Tcikti.append("Hata: Lütfen (Manning Kat Sayısı (n)) Sütununu Seçiniz!")
            return False

            
        
        # Gerekli alanların eklenmesi
        fields_to_add = [
            ("KotFarkı", QVariant.Double),
            ("BoruEğimi", QVariant.Double),
            ("DoluHalde(Qd)", QVariant.Double),
            ("DoluHalde(Vd)", QVariant.Double),
            ("Boyutsuz(Qh/Qd)", QVariant.Double),
            ("Boyutsuz(V/Vd)", QVariant.Double),
            ("Boyutsuz(h/D)", QVariant.Double),
            ("HesapDebisi(V)", QVariant.Double),
            ("HesapDebisi(H)", QVariant.Double),
            ("GeotekstilAlani", QVariant.Double),
        ]
        
        if self.addFieldsToLayer(selected_layer, fields_to_add):
            self.dlg.Tcikti.append("Alanlar başarıyla eklendi!")
        else:
            self.dlg.Tcikti.append("Alanlar eklenirken bir sorun oluştu.")
        
        for feature in selected_layer.getFeatures():
            
            
            try:
                boruBas = feature[cbboruKotBaslangic] if cbboruKotBaslangic in feature.fields().names() else None
                boruSon = feature[cbboruKotSon] if cbboruKotSon in feature.fields().names() else None
                cap = feature[cbcap] if cbcap in feature.fields().names() else None
                manning = feature[cbmanning] if cbmanning in feature.fields().names() else None
                uzunluk = feature["Uzunluk"] if "Uzunluk" in feature.fields().names() else None
                debi = feature["Debi"] if "Debi" in feature.fields().names() else None
                
                if None in [boruBas, boruSon, cap, manning, uzunluk, debi]:
                    self.dlg.Tcikti.append("Hata: Veriler eksik veya hatalı!")
                    continue
                
                # Hesaplamalar
                kotFarki = boruBas - boruSon
                boruEgimi = kotFarki / uzunluk if uzunluk != 0 else  None
                if uzunluk == 0:
                    self.dlg.Tcikti.append(f"{uzunluk} 0 oldu, {feature.id()} idli satırda hata!")
                    return False
                
                """
                # Sonuçları yazdır
                self.dlg.Tcikti.append(f"kotFarki: {kotFarki}")
                self.dlg.Tcikti.append(f"boruEgimi: {boruEgimi}")
                """
                doluHaldeQd = (math.pi*pow((cap/1000),2)/4/manning*pow((cap/4000),2/3)*pow(boruEgimi, 0.5))*1000
                doluHaldeVd = (pow((cap/4000),2/3)*pow(boruEgimi,0.5)/manning)
                """
                # Sonuçları yazdır
                self.dlg.Tcikti.append(f"doluHaldeQd: {doluHaldeQd}")
                self.dlg.Tcikti.append(f"doluHaldeVd: {doluHaldeVd}")
                """
                boyutsuzelemanlarQhQd = debi/doluHaldeQd if doluHaldeQd != 0 else  None
                
                boyutsuzelemanlarVVd = 0.162+14.671*boyutsuzelemanlarQhQd-217.329*pow(boyutsuzelemanlarQhQd,2)+1903.829*pow(boyutsuzelemanlarQhQd,3) \
                -9790.558*pow(boyutsuzelemanlarQhQd,4)+31070.169*pow(boyutsuzelemanlarQhQd,5)-62603.012*pow(boyutsuzelemanlarQhQd,6) \
                +80217.184*pow(boyutsuzelemanlarQhQd,7)-63292.361*pow(boyutsuzelemanlarQhQd,8)+28028.438*pow(boyutsuzelemanlarQhQd,9) \
                -5330.194*pow(boyutsuzelemanlarQhQd,10)
                
                boyutsuzelemanlarHD = 0.025+4.201*boyutsuzelemanlarQhQd-45.157*pow(boyutsuzelemanlarQhQd,2)+329.79*pow(boyutsuzelemanlarQhQd,3) \
                -1402.057*pow(boyutsuzelemanlarQhQd,4)+3567.375*pow(boyutsuzelemanlarQhQd,5)-5459.571*pow(boyutsuzelemanlarQhQd,6) \
                +4816.746*pow(boyutsuzelemanlarQhQd,7)-2095.414*pow(boyutsuzelemanlarQhQd,8)+174.327*pow(boyutsuzelemanlarQhQd,9) \
                +110.718*pow(boyutsuzelemanlarQhQd,10)
                
                if boyutsuzelemanlarHD > 0.5:
                    self.dlg.Tcikti.append(f"{feature.id()} idli işlemde Boyutsuz Hidrolik Elemanları (h/D) hesabı 0.5'ten büyük olmamalıdır !!!")

                
                """
                # Sonuçları yazdır
                self.dlg.Tcikti.append(f"boyutsuzelemanlarQhQd: {boyutsuzelemanlarQhQd}")
                self.dlg.Tcikti.append(f"boyutsuzelemanlarVVd: {boyutsuzelemanlarVVd}")
                self.dlg.Tcikti.append(f"boyutsuzelemanlarHD: {boyutsuzelemanlarHD}")
                """
                hesapdebisiV = doluHaldeVd * boyutsuzelemanlarVVd
                hesapdebisiH = cap * boyutsuzelemanlarHD
                
                """
                # Sonuçları yazdır
                self.dlg.Tcikti.append(f"hesapdebisiV: {hesapdebisiV}")
                self.dlg.Tcikti.append(f"hesapdebisiH: {hesapdebisiH}")
                """
                geotekstilAlani = uzunluk * (math.pi*cap/1000)
                
                """
                self.dlg.Tcikti.append(f"geotekstilAlani: {geotekstilAlani}")
                """
                
                # Özellikleri güncelle
                attrs = {
                    selected_layer.fields().lookupField("KotFarkı"): kotFarki,
                    selected_layer.fields().lookupField("BoruEğimi"): boruEgimi,
                    selected_layer.fields().lookupField("DoluHalde(Qd)"): doluHaldeQd,
                    selected_layer.fields().lookupField("DoluHalde(Vd)"): doluHaldeVd,
                    selected_layer.fields().lookupField("Boyutsuz(Qh/Qd)"): boyutsuzelemanlarQhQd,
                    selected_layer.fields().lookupField("Boyutsuz(V/Vd)"): boyutsuzelemanlarVVd,
                    selected_layer.fields().lookupField("Boyutsuz(h/D)"): boyutsuzelemanlarHD,
                    selected_layer.fields().lookupField("HesapDebisi(V)"): hesapdebisiV,
                    selected_layer.fields().lookupField("HesapDebisi(H)"): hesapdebisiH,
                    selected_layer.fields().lookupField("GeotekstilAlani"): geotekstilAlani,
                    
                }
                
                try:
                    with edit(selected_layer):
                        selected_layer.dataProvider().changeAttributeValues({feature.id(): attrs})
                    
                except Exception as e:
                    self.dlg.Tcikti.append(f"DİKKAT!!! - Feature {feature.id()} güncellenirken hata oluştu !!!")
                
            except (TypeError, ValueError) as e:
                    self.dlg.Tcikti.append(f"Hata: {e}")
                    self.dlg.Tcikti.append("-" * 20)
        
        self.dlg.Tcikti.append("Hesaplama işlemi gerçekleşti.")
        # Katmanın görsel güncellenmesi için
        selected_layer.triggerRepaint()
        self.dlg.Tcikti.append("-" * 20)
        return True
    def __kaziHacmiHesaplama(self):
        # Seçili katmanı al
        selected_layer = self.dlg.CBLayer.currentLayer()

        # Eğer hiçbir şey seçilmemişse, hata mesajını Tcikti'ye yazdır
        if selected_layer is None:
            self.dlg.Tcikti.append("Hata: Lütfen geçerli bir katman seçin!")
            return

        # Eğer bir katman seçilmişse, seçilen katman adını Tcikti'ye yazdır
        self.dlg.Tcikti.append(f"Seçili Katman: {selected_layer.name()}")

        cbboruKotBaslangic = self.dlg.CBboruKotBaslangic.currentText()
        cbboruKotSon = self.dlg.CBboruKotSon.currentText()
        cbcap = self.dlg.CBcap.currentText()
        
        if not cbboruKotBaslangic or cbboruKotBaslangic == "Seçiniz":
            self.dlg.Tcikti.append("Hata: Lütfen (Boru Taban Kot Başlangıcı) Sütununu Seçiniz!")
            return False
        if not cbboruKotSon or cbboruKotSon == "Seçiniz":
            self.dlg.Tcikti.append("Hata: Lütfen (Boru Taban Kot Son) Sütununu Seçiniz!")
            return False
        if not cbcap or cbcap == "Seçiniz":
            self.dlg.Tcikti.append("Hata: Lütfen (Çap (mm)) Sütununu Seçiniz!")
            return False
        
        if self.dlg.RBdem.isChecked():
            
            selected_demlayer = self.dlg.CBDemLayer.currentLayer()
        
            if selected_demlayer is None:
                self.dlg.Tcikti.append("Hata: Lütfen bir DEM katmanı seçin!")
                return False
            
            # TIFF olup olmadığını kontrol et
            data_source = selected_demlayer.dataProvider().dataSourceUri()
            if not data_source.lower().endswith('.tif'):
                self.dlg.Tcikti.append("Hata: Seçilen DEM katmanı bir TIFF dosyası değil!")
                return False
            
            # Mesajı Tcikti'ye yazdır
            self.dlg.Tcikti.append(f"Seçili Katman: {selected_demlayer.name()}")
            
        elif self.dlg.RBzemin.isChecked():
                
            cbzeminKotBas = self.dlg.CBzeminKotBas.currentText()
            cbzeminKotSon = self.dlg.CBzeminKotSon.currentText()
            
            if not cbzeminKotBas or cbzeminKotBas == "Seçiniz":
                self.dlg.Tcikti.append("Hata: Lütfen (Zemin Kot Başlangıç) Sütununu Seçiniz!")
                return False
            if not cbzeminKotSon or cbzeminKotSon == "Seçiniz":
                self.dlg.Tcikti.append("Hata: Lütfen (Zemin Kot Son) Sütununu Seçiniz!")
                return False
        else:
            self.dlg.Tcikti.append("Lütfen Kazı Hacmi Hesaplamaları için Dem dosyası ya da Zemin Kot Sütunlarından birini seçiniz !!!")
            return False
        
        # Gerekli alanların eklenmesi
        fields_to_add = [
            ("ZeminKotBas", QVariant.Double),
            ("ZeminKotSon", QVariant.Double),
            ("KazıHacmiBas", QVariant.Double),
            ("KazıHacmiSon", QVariant.Double),
            ("KazıHacmiGen", QVariant.Double),
            ("KazıHAcmiHacim", QVariant.Double),
        ]
        
        if self.addFieldsToLayer(selected_layer, fields_to_add):
            self.dlg.Tcikti.append("Alanlar başarıyla eklendi!")
        else:
            self.dlg.Tcikti.append("Alanlar eklenirken bir sorun oluştu.")
        
        for feature in selected_layer.getFeatures():
            
            
            try:
                boruBas = feature[cbboruKotBaslangic] if cbboruKotBaslangic in feature.fields().names() else None
                boruSon = feature[cbboruKotSon] if cbboruKotSon in feature.fields().names() else None
                cap = feature[cbcap] if cbcap in feature.fields().names() else None
                uzunluk = feature["Uzunluk"] if "Uzunluk" in feature.fields().names() else None
                
                if None in [boruBas, boruSon, cap, uzunluk]:
                    self.dlg.Tcikti.append("Hata: Veriler eksik veya hatalı!")
                    continue
                
                
                if self.dlg.RBdem.isChecked():
                    geometry = feature.geometry()
                    
                    line = geometry.asPolyline()
                    
                    
                    if line:  # Geometri varsa
                        
                        start_point = line[0]
                        end_point = line[-1]
                        """
                        self.dlg.Tcikti.append(f"Vektör ID: {feature.id()} BU işlem RBdemde hesaplandı")
                        self.dlg.Tcikti.append(f"Vektör ID: {feature.id()} - Başlangıç: {start_point}, Bitiş: {end_point}")
                        """
                        def get_elevation_at_point(point):
                        # Nokta koordinatındaki yükseklik değerini al
                            elev  = selected_demlayer.dataProvider().sample(point, 1)  # 1, tek bandı ifade eder
                            return elev

                        # Başlangıç ve bitiş noktalarındaki yükseklikleri al
                        YBasdem = get_elevation_at_point(start_point)
                        YSondem = get_elevation_at_point(end_point)
                        """
                        self.dlg.Tcikti.append(f"Vektör ID: {feature.id()}")
                        self.dlg.Tcikti.append(f"Başlangıç Yüksekliği (YBas): {YBasdem}")
                        self.dlg.Tcikti.append(f"Bitiş Yüksekliği (YSon): {YSondem}")
                        """
                        if isinstance(YBasdem, tuple):
                            YBasdem = YBasdem[0]
                        if isinstance(YSondem, tuple):
                            YSondem = YSondem[0]

                        kaziHacmiBas = YBasdem - boruBas
                        kaziHacmiSon = YSondem - boruSon
                        
                        
                        
                        
                    
                elif self.dlg.RBzemin.isChecked():
                        zeminKotBas = feature[cbzeminKotBas] if cbzeminKotBas in feature.fields().names() else None
                        zeminKotSon = feature[cbzeminKotSon] if cbzeminKotSon in feature.fields().names() else None

                        kaziHacmiBas = zeminKotBas - boruBas
                        kaziHacmiSon = zeminKotSon - boruSon
                        
                    
                else:
                    self.dlg.Tcikti.append("Seçilmedi.")
                    return False
                
                kaziHacmiGen = 0
                kaziHacmiGen = (cap+200)/1000
                kaziHacmiHacim = ((kaziHacmiBas + 0.15 + kaziHacmiSon + 0.15)/2)*uzunluk*kaziHacmiGen
                
                """
                self.dlg.Tcikti.append(f"kaziHacmiBas: {kaziHacmiBas}")
                self.dlg.Tcikti.append(f"kaziHacmiSon: {kaziHacmiSon}")
                self.dlg.Tcikti.append(f"kaziHacmiSon: {kaziHacmiGen}")
                self.dlg.Tcikti.append(f"kaziHacmiHacim: {kaziHacmiHacim}")
                """
                
                if self.dlg.RBdem.isChecked():
                    attrs = {
                        selected_layer.fields().lookupField("ZeminKotBas"): YBasdem,
                        selected_layer.fields().lookupField("ZeminKotSon"): YSondem,
                        selected_layer.fields().lookupField("KazıHacmiBas"): kaziHacmiBas,
                        selected_layer.fields().lookupField("KazıHacmiSon"): kaziHacmiSon,
                        selected_layer.fields().lookupField("KazıHacmiGen"): kaziHacmiGen,
                        selected_layer.fields().lookupField("KazıHAcmiHacim"): kaziHacmiHacim,
                    
                    }
                else:
                    attrs = {
                        selected_layer.fields().lookupField("KazıHacmiBas"): kaziHacmiBas,
                        selected_layer.fields().lookupField("KazıHacmiSon"): kaziHacmiSon,
                        selected_layer.fields().lookupField("KazıHacmiGen"): kaziHacmiGen,
                        selected_layer.fields().lookupField("KazıHAcmiHacim"): kaziHacmiHacim,
                    }

                
                try:
                    with edit(selected_layer):
                        selected_layer.dataProvider().changeAttributeValues({feature.id(): attrs})
                    
                except Exception as e:
                    self.dlg.Tcikti.append(f"DİKKAT!!! - Feature {feature.id()} güncellenirken hata oluştu !!!")
                
                
            except (TypeError, ValueError):
                self.dlg.Tcikti.append(f"Hata: {e}")
                self.dlg.Tcikti.append("-" * 20)
        
        self.dlg.Tcikti.append("Hesaplama işlemi gerçekleşti.")
        # Katmanın görsel güncellenmesi için
        selected_layer.triggerRepaint()
        self.dlg.Tcikti.append("-" * 20)   
        return True
    
    def __getSelectedLayer(self):
        """Seçili katman döndüren yardımcı fonksiyon."""
        selected_layer = self.dlg.CBLayer.currentLayer()
        
        # Katman türüne göre işlem yap
        if selected_layer.type() == QgsMapLayer.VectorLayer:
            self.dlg.Tcikti.append(f"Seçili Katman: {selected_layer.name()} ")
        elif selected_layer.type() == QgsMapLayer.RasterLayer:
            self.dlg.Tcikti.append("Hata: Raster katman seçilemez, vektör katmanı seçin.")
            return None
        else:
            self.dlg.Tcikti.append("Hata: Bilinmeyen katman türü!")
            return None

        return selected_layer


    def __attributeSutunGet(self):
        """Vektör katmanındaki sütunları QComboBox'a ekler."""
        # Seçili katmanı al
        selected_layer = self.__getSelectedLayer()
        if selected_layer is None:
            self.dlg.Tcikti.append("Hata: Katman seçilmedi!")
            return  False

        # Katman türünü kontrol et
        if not isinstance(selected_layer, QgsVectorLayer):
            self.dlg.Tcikti.append("Hata: Seçilen katman bir vektör katmanı değil!")
            return False
    
        fields = selected_layer.fields()  # Vektör katmanı için alanları al
        column_names = [field.name() for field in fields]
        
        # QComboBox'ları temizle ve sütun isimlerini ekle
        combo_boxes = [
            self.dlg.CBboruBaslangic,
            self.dlg.CBboruSon,
            self.dlg.CBdrenGen,
            self.dlg.CBzeminKotBas,
            self.dlg.CBzeminKotSon,
            self.dlg.CBboruKotBaslangic,
            self.dlg.CBboruKotSon,
            self.dlg.CBcap,
            self.dlg.CBmanning,
            
        ]
        
        # Her ComboBox için işlem
        for combo_box in combo_boxes:
            combo_box.clear()
            combo_box.addItem("Seçiniz")  # İlk seçenek olarak "Seçiniz" ekle
            
            # Sütun adlarını ekle
            combo_box.addItems(column_names)
            combo_box.setCurrentIndex(0)
            
            # "fid" ve "id" değerlerini kaldır
            for text in ["fid", "id"]:
                index = combo_box.findText(text)
                if index != -1:
                    combo_box.removeItem(index)
                    
        self.dlg.CBzeminKotBas.setEnabled(False)  
        self.dlg.CBzeminKotSon.setEnabled(False)
        self.dlg.CBDemLayer.setEnabled(False)


    def __alanHesapla(self):
        """Alan hesaplamasını gerçekleştiren fonksiyon."""
        selected_layer = self.__getSelectedLayer()
        if selected_layer is None:
            return  False
        
        
        
        cbBoruBaslangic = self.dlg.CBboruBaslangic.currentText()
        cbBoruSon = self.dlg.CBboruSon.currentText()
        cbDrenGen = self.dlg.CBdrenGen.currentText()

        if not cbBoruBaslangic or cbBoruBaslangic == "Seçiniz":
            self.dlg.Tcikti.append("Hata: Lütfen (Boru Başlangıcı) Sütununu Seçiniz!")
            return False
        if not cbBoruSon or cbBoruSon == "Seçiniz":
            self.dlg.Tcikti.append("Hata: Lütfen (Boru Sonu) Sütununu Seçiniz!")
            return False
        if not cbDrenGen or cbDrenGen == "Seçiniz":
            self.dlg.Tcikti.append("Hata: Lütfen (Dren Genişliği) Sütununu Seçiniz!")
            return False
        if not self.dlg.LEdebiKatsayisi.text():
            self.dlg.Tcikti.append("Hata: Lütfen (Debi Kat Sayısı) Boş Bırakılamaz!")
            return False
        
        try:
            debiKatsayisi = float(self.dlg.LEdebiKatsayisi.text())
        except ValueError:
            self.dlg.Tcikti.append("Hata: Geçerli bir debi katsayısı girin!\nVirgül yerine nokta kullanmaya dikkat edin!!!")
            return False
        
        

        ustalanlistesi = {}  # Üst alanlar için dictionary
        boruuclarlistesi = {}
        
        # Gerekli alanların eklenmesi
        fields_to_add = [
            ("Uzunluk", QVariant.Double),
            ("KismiAlan", QVariant.Double),
            ("UstAlan", QVariant.Double),
            ("ToplamAlan", QVariant.Double),
            ("Debi", QVariant.Double),
        ]
        
        if self.addFieldsToLayer(selected_layer, fields_to_add):
            self.dlg.Tcikti.append("Alanlar başarıyla eklendi!")
        else:
            self.dlg.Tcikti.append("Alanlar eklenirken bir sorun oluştu.")
            
            
        hataVarmi = False
        for feature in selected_layer.getFeatures():
            geometry = feature.geometry()
            length = geometry.length()
           
            
            bas = feature[cbBoruBaslangic]
            son = feature[cbBoruSon]
            
            if bas == son:
                self.dlg.Tcikti.append(f"{feature.id()}:.ID borunun bas ve son noktaları aynı olamaz")
                hataVarmi = True
            if bas in boruuclarlistesi.keys():
                self.dlg.Tcikti.append(f"{feature.id()}:.ID borunun baş noktasi başka boru ile aynı.")
                hataVarmi = True
                
            boruuclarlistesi[bas] = son
            drengen = float(feature[cbDrenGen])
            

            kismiAlan = drengen * length
            
            # Üst alanları hesapla
            if bas in ustalanlistesi.keys():
                UstAlan = ustalanlistesi[bas]
            else:
                UstAlan = 0
            ToplamAlan = UstAlan + kismiAlan
            if son in ustalanlistesi.keys():
                ustalanlistesi[son] = ustalanlistesi[son] + ToplamAlan
                while son in boruuclarlistesi.keys():
                    son = boruuclarlistesi[son]
                    ustalanlistesi[son] = ustalanlistesi[son] + kismiAlan
            else:
                ustalanlistesi[son] = ToplamAlan

        if hataVarmi == True:
            return None
        
        for feature in selected_layer.getFeatures():
            geometry = feature.geometry()
            length = geometry.length()
            bas = feature[cbBoruBaslangic]
            son = feature[cbBoruSon]
            drengen = float(feature[cbDrenGen])
            
            if bas in ustalanlistesi:
                UstAlan = ustalanlistesi[bas]
            else:
                UstAlan = 0
            
            kismiAlan = drengen * length
            ToplamAlan = UstAlan + kismiAlan
            Debi = ToplamAlan * debiKatsayisi
            
            
                # Özellikleri güncelle
            attrs = {
                selected_layer.fields().lookupField("Uzunluk"): length,
                selected_layer.fields().lookupField("KismiAlan"): kismiAlan,
                selected_layer.fields().lookupField("UstAlan"): UstAlan,
                selected_layer.fields().lookupField("ToplamAlan"): ToplamAlan,
                selected_layer.fields().lookupField("Debi"): Debi,
            }
            try:
                with edit(selected_layer):
                    selected_layer.dataProvider().changeAttributeValues({feature.id(): attrs})
                
            except Exception as e:
                self.dlg.Tcikti.append(f"DİKKAT!!! - Feature {feature.id()} güncellenirken hata oluştu: {str(e)}")


        self.dlg.Tcikti.append("Hesaplama işlemi gerçekleşti.")
        # Katmanın görsel güncellenmesi için
        selected_layer.triggerRepaint()
        self.dlg.Tcikti.append("-" * 20)
        return True

    def addFieldsToLayer(self, selected_layer, fields_to_add):
        
        if selected_layer is None:
            self.dlg.Tcikti.append("Hata: Katman seçilmedi.")
            
            return False

        # Katmanı düzenleme moduna al ve alanları ekle
        try:
            with edit(selected_layer):
                for field_name, field_type in fields_to_add:
                    if field_name not in [field.name() for field in selected_layer.fields()]:
                        selected_layer.dataProvider().addAttributes([QgsField(field_name, field_type)])
                selected_layer.updateFields()
            return True
        except Exception as e:
            self.dlg.Tcikti.append("Hata: Alanlar eklenirken bir sorun oluştu. {e}")
            return False
       
    
    
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Hidrolik Hesaplayici'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
