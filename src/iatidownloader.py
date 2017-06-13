# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import urllib2
import urllib
import os
import errno
import re
import uuid

regions = {
88:'States Ex-Yugoslavia, unspecified',
89:'Europe, regional',
189:'North of Sahara, regional',
289:'South of Sahara, regional' ,
298:'Africa, regional',
380:'West Indies, regional' ,
389:'North and Central America, regional',
489:'South America, regional',
498:'America, regional',
589:'Middle East, regional'  ,
619:'Central Asia, regional'  ,
679:'South Asia, regional',
689:'South and Central Asia, regional'  ,
789:'Far East Asia, regional',
798:'Asia, regional',
889:'Oceania, regional'   ,
998:'Developing countries, unspecified'
}



countries={'AF' :'AFGHANISTAN' ,
'AX' :'ALAND ISLANDS' ,
'AL' :'ALBANIA' ,
'DZ' :'ALGERIA' ,
'AS' :'AMERICAN SAMOA' ,
'AD' :'ANDORRA' ,
'AO' :'ANGOLA' ,
'AI' :'ANGUILLA' ,
'AQ' :'ANTARCTICA' ,
'AG' :'ANTIGUA AND BARBUDA' ,
'AR' :'ARGENTINA' ,
'AM' :'ARMENIA' ,
'AW' :'ARUBA' ,
'AU' :'AUSTRALIA' ,
'AT' :'AUSTRIA' ,
'AZ' :'AZERBAIJAN' ,
'BS' :'BAHAMAS (THE)' ,
'BH' :'BAHRAIN' ,
'BD' :'BANGLADESH' ,
'BB' :'BARBADOS' ,
'BY' :'BELARUS' ,
'BE' :'BELGIUM' ,
'BZ' :'BELIZE' ,
'BJ' :'BENIN' ,
'BM' :'BERMUDA' ,
'BT' :'BHUTAN' ,
'BO' :'BOLIVIA (PLURINATIONAL STATE OF)' ,
'BQ' :'BONAIRE, SAINT EUSTATIUS AND SABA' ,
'BA' :'BOSNIA AND HERZEGOVINA' ,
'BW' :'BOTSWANA' ,
'BV' :'BOUVET ISLAND' ,
'BR' :'BRAZIL' ,
'IO' :'BRITISH INDIAN OCEAN TERRITORY (THE)' ,
'BN' :'BRUNEI DARUSSALAM' ,
'BG' :'BULGARIA' ,
'BF' :'BURKINA FASO' ,
'BI' :'BURUNDI' ,
'KH' :'CAMBODIA' ,
'CM' :'CAMEROON' ,
'CA' :'CANADA' ,
'CV' :'CAPE VERDE' ,
'KY' :'CAYMAN ISLANDS (THE)' ,
'CF' :'CENTRAL AFRICAN REPUBLIC (THE)' ,
'TD' :'CHAD' ,
'CL' :'CHILE' ,
'CN' :'CHINA' ,
'CX' :'CHRISTMAS ISLAND' ,
'CC' :'COCOS (KEELING) ISLANDS (THE)' ,
'CO' :'COLOMBIA' ,
'KM' :'COMOROS (THE)' ,
'CG' :'CONGO (THE)' ,
'CD' :'CONGO, THE DEMOCRATIC REPUBLIC OF THE' ,
'CK' :'COOK ISLANDS (THE)' ,
'CR' :'COSTA RICA' ,
'CI' :'CÔTE D’IVOIRE' ,
'HR' :'CROATIA' ,
'CU' :'CUBA' ,
'CW' :'CURAÇAO' ,
'CY' :'CYPRUS' ,
'CZ' :'CZECH REPUBLIC (THE)' ,
'DK' :'DENMARK' ,
'DJ' :'DJIBOUTI' ,
'DM' :'DOMINICA' ,
'DO' :'DOMINICAN REPUBLIC (THE)' ,
'EC' :'ECUADOR' ,
'EG' :'EGYPT' ,
'SV' :'EL SALVADOR' ,
'GQ' :'EQUATORIAL GUINEA' ,
'ER' :'ERITREA' ,
'EE' :'ESTONIA' ,
'ET' :'ETHIOPIA' ,
'FK' :'FALKLAND ISLANDS (THE) [MALVINAS]' ,
'FO' :'FAROE ISLANDS (THE)' ,
'FJ' :'FIJI' ,
'FI' :'FINLAND' ,
'FR' :'FRANCE' ,
'GF' :'FRENCH GUIANA' ,
'PF' :'FRENCH POLYNESIA' ,
'TF' :'FRENCH SOUTHERN TERRITORIES (THE)' ,
'GA' :'GABON' ,
'GM' :'GAMBIA (THE)' ,
'GE' :'GEORGIA' ,
'DE' :'GERMANY' ,
'GH' :'GHANA' ,
'GI' :'GIBRALTAR' ,
'GR' :'GREECE' ,
'GL' :'GREENLAND' ,
'GD' :'GRENADA' ,
'GP' :'GUADELOUPE' ,
'GU' :'GUAM' ,
'GT' :'GUATEMALA' ,
'GG' :'GUERNSEY' ,
'GN' :'GUINEA' ,
'GW' :'GUINEA-BISSAU' ,
'GY' :'GUYANA' ,
'HT' :'HAITI' ,
'HM' :'HEARD ISLAND AND MCDONALD ISLANDS' ,
'VA' :'HOLY SEE (THE)' ,
'HN' :'HONDURAS' ,
'HK' :'HONG KONG' ,
'HU' :'HUNGARY' ,
'IS' :'ICELAND' ,
'IN' :'INDIA' ,
'ID' :'INDONESIA' ,
'IR' :'IRAN (ISLAMIC REPUBLIC OF)' ,
'IQ' :'IRAQ' ,
'IE' :'IRELAND' ,
'IM' :'ISLE OF MAN' ,
'IL' :'ISRAEL' ,
'IT' :'ITALY' ,
'JM' :'JAMAICA' ,
'JP' :'JAPAN' ,
'JE' :'JERSEY' ,
'JO' :'JORDAN' ,
'KZ' :'KAZAKHSTAN' ,
'KE' :'KENYA' ,
'KI' :'KIRIBATI' ,
'KP' :'KOREA (DEMOCRATIC PEOPLE’S REPUBLIC OF)' ,
'KR' :'KOREA (REPUBLIC OF)' ,
'XK' :'KOSOVO' ,
'KW' :'KUWAIT' ,
'KG' :'KYRGYZSTAN' ,
'LA' :'LAO PEOPLE’S DEMOCRATIC REPUBLIC (THE)' ,
'LV' :'LATVIA' ,
'LB' :'LEBANON' ,
'LS' :'LESOTHO' ,
'LR' :'LIBERIA' ,
'LY' :'LIBYAN ARAB JAMAHIRIYA' ,
'LI' :'LIECHTENSTEIN' ,
'LT' :'LITHUANIA' ,
'LU' :'LUXEMBOURG' ,
'MO' :'MACAO' ,
'MK' :'MACEDONIA (THE FORMER YUGOSLAV REPUBLIC OF)' ,
'MG' :'MADAGASCAR' ,
'MW' :'MALAWI' ,
'MY' :'MALAYSIA' ,
'MV' :'MALDIVES' ,
'ML' :'MALI' ,
'MT' :'MALTA' ,
'MH' :'MARSHALL ISLANDS (THE)' ,
'MQ' :'MARTINIQUE' ,
'MR' :'MAURITANIA' ,
'MU' :'MAURITIUS' ,
'YT' :'MAYOTTE' ,
'MX' :'MEXICO' ,
'FM' :'MICRONESIA (FEDERATED STATES OF)' ,
'MD' :'MOLDOVA (REPUBLIC OF)' ,
'MC' :'MONACO' ,
'MN' :'MONGOLIA' ,
'ME' :'MONTENEGRO' ,
'MS' :'MONTSERRAT' ,
'MA' :'MOROCCO' ,
'MZ' :'MOZAMBIQUE' ,
'MM' :'MYANMAR' ,
'NA' :'NAMIBIA' ,
'NR' :'NAURU' ,
'NP' :'NEPAL' ,
'NL' :'NETHERLANDS (THE)' ,
'AN' :'NETHERLAND ANTILLES' ,
'NC' :'NEW CALEDONIA' ,
'NZ' :'NEW ZEALAND' ,
'NI' :'NICARAGUA' ,
'NE' :'NIGER (THE)' ,
'NG' :'NIGERIA' ,
'NU' :'NIUE' ,
'NF' :'NORFOLK ISLAND' ,
'MP' :'NORTHERN MARIANA ISLANDS (THE)' ,
'NO' :'NORWAY' ,
'OM' :'OMAN' ,
'PK' :'PAKISTAN' ,
'PW' :'PALAU' ,
'PS' :'PALESTINIAN TERRITORY, OCCUPIED' ,
'PA' :'PANAMA' ,
'PG' :'PAPUA NEW GUINEA' ,
'PY' :'PARAGUAY' ,
'PE' :'PERU' ,
'PH' :'PHILIPPINES (THE)' ,
'PN' :'PITCAIRN' ,
'PL' :'POLAND' ,
'PT' :'PORTUGAL' ,
'PR' :'PUERTO RICO' ,
'QA' :'QATAR' ,
'RE' :'REUNION' ,
'RO' :'ROMANIA' ,
'RU' :'RUSSIAN FEDERATION (THE)' ,
'RW' :'RWANDA' ,
'BL' :'SAINT BARTHÉLEMY' ,
'SH' :'SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA' ,
'KN' :'SAINT KITTS AND NEVIS' ,
'LC' :'SAINT LUCIA' ,
'MF' :'SAINT MARTIN (FRENCH PART)' ,
'PM' :'SAINT PIERRE AND MIQUELON' ,
'VC' :'SAINT VINCENT AND THE GRENADINES' ,
'WS' :'SAMOA' ,
'SM' :'SAN MARINO' ,
'ST' :'SAO TOME AND PRINCIPE' ,
'SA' :'SAUDI ARABIA' ,
'SN' :'SENEGAL' ,
'RS' :'SERBIA' ,
'SC' :'SEYCHELLES' ,
'SL' :'SIERRA LEONE' ,
'SG' :'SINGAPORE' ,
'SX' :'SINT MAARTEN (DUTCH PART)' ,
'SK' :'SLOVAKIA' ,
'SI' :'SLOVENIA' ,
'SB' :'SOLOMON ISLANDS' ,
'SO' :'SOMALIA' ,
'ZA' :'SOUTH AFRICA' ,
'GS' :'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS' ,
'SS' :'SOUTH SUDAN' ,
'ES' :'SPAIN' ,
'LK' :'SRI LANKA' ,
'SD' :'SUDAN (THE)' ,
'SR' :'SURINAME' ,
'SJ' :'SVALBARD AND JAN MAYEN' ,
'SZ' :'SWAZILAND' ,
'SE' :'SWEDEN' ,
'CH' :'SWITZERLAND' ,
'SY' :'SYRIAN ARAB REPUBLIC' ,
'TW' :'TAIWAN (PROVINCE OF CHINA)' ,
'TJ' :'TAJIKISTAN' ,
'TZ' :'TANZANIA, UNITED REPUBLIC OF' ,
'TH' :'THAILAND' ,
'TL' :'TIMOR-LESTE' ,
'TG' :'TOGO' ,
'TK' :'TOKELAU' ,
'TO' :'TONGA' ,
'TT' :'TRINIDAD AND TOBAGO' ,
'TN' :'TUNISIA' ,
'TR' :'TURKEY' ,
'TM' :'TURKMENISTAN' ,
'TC' :'TURKS AND CAICOS ISLANDS (THE)' ,
'TV' :'TUVALU' ,
'UG' :'UGANDA' ,
'UA' :'UKRAINE' ,
'AE' :'UNITED ARAB EMIRATES (THE)' ,
'GB' :'UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND (THE)' ,
'US' :'UNITED STATES OF AMERICA (THE)' ,
'UM' :'UNITED STATES MINOR OUTLYING ISLANDS (THE)' ,
'UY' :'URUGUAY' ,
'UZ' :'UZBEKISTAN' ,
'VU' :'VANUATU' ,
'VE' :'VENEZUELA (BOLIVARIAN REPUBLIC OF)' ,
'VN' :'VIET NAM' ,
'VG' :'VIRGIN ISLANDS (BRITISH)' ,
'VI' :'VIRGIN ISLANDS (U.S.)' ,
'WF' :'WALLIS AND FUTUNA' ,
'EH' :'WESTERN SAHARA' ,
'YE' :'YEMEN' ,
'ZM' :'ZAMBIA' ,
'ZW' :'ZIMBABWE' }


organisations={
    'GB-GOV':'DIFD',
    '46002':'AFDB'
}


def get_folder_name(name):
    return re.sub(re.compile('[^0-9a-zA-Z]+'), '_', name).lower()


def create_folder(path, name):
    target = '%s/%s' % (path , name)
    if not os.path.exists(os.path.abspath(target)):
            try:
                os.makedirs(os.path.abspath(target))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
    return target
                

def download(dest_path,url):
    try:
        file_name=url.split('/')[-1]
        f=urllib2.urlopen(url)
        if 'text' in f.info().maintype:
            md='w'
            if 'html' in f.info().getsubtype():
                file_name='%s.html' % uuid.uuid1()
        else:
            md='wb'    
            
       
            with open("%s/%s" % (dest_path, file_name), md) as local_file:
                local_file.write(f.read())
                print 'file saved'
    except Exception as inst:
        print(inst.message)
    

def process_activity(act_doc,org):
    
    ##check for 07 and 02 documents 
    if len(act_doc.findall("document-link/category[@code='A02']") + act_doc.findall("document-link/category[@code='A07']")) > 0 :
        identifier = act_doc.find('iati-identifier').text
       
        print 'Activity %s has documents we will process it ' % identifier 
       
        region_code = int(act_doc.find('recipient-region').get('code')) if act_doc.find('recipient-region') != None else None
        country_code = act_doc.find('recipient-country').get('code') if act_doc.find('recipient-country') != None else None
        
        folder = 'NA'
       
        if (countries[country_code] != None):
            folder = get_folder_name(countries[country_code])
        elif(regions[region_code] != None):
            folder = get_folder_name(regions[region_code])
         
        path = create_folder('../projects/%s' % organisations[org], folder)
        
        path = create_folder(path, identifier)
                 
        print 'Saving xml file %s' % identifier
        xml = '%s/activity.xml' % path
        
        f = open(xml, 'w')
        f.write(ET.tostring(act_doc))
        f.close() 
        
        print 'Getting related documents'
        
        docs = act_doc.findall('document-link')
        
        for doc in docs:
            if doc.findall("category[@code='A02']")!=None or doc.findall("category[@code='A07']")!=None:
                download(path,doc.get('url'))
    else:
        print "Activity %s hasn't any doc type A02 or A07"     


def data_download(org,country,offset=0,limit=100):
    url = 'http://datastore.iatistandard.org/api/1/access/activity.xml?reporting-org=%s&recipient-country=%s&offset=0&limit=%s' % (org,country,limit)
    root = ET.parse(urllib.urlopen(url)).getroot()
    activites = root.findall('iati-activities/iati-activity')
    print(len(activites))
    [(process_activity(activity,org)) for activity in activites]

for country in countries:
        data_download('46002',country,0,500)
    
  
    


    
    
