#-*- coding:utf-8 -*-
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time

import numpy as np
import matplotlib.pyplot as plt
import mpld3

import pymysql

import pandas as pd


seq_pieces_charge = []
x_axis = ['C_terminus']
error_id_array = []

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options) #드라이버 정의


# #uniprot ID 반환
# def get_uniprot_accession_id(response_xml):
#     parser = etree.XMLParser(recover=True)
#     root = ET.fromstring(response_xml, parser=parser)
#     return next(
#         el for el in root.getchildren()[0].getchildren()
#         if el.attrib['dbSource'] == 'UniProt'
#     ).attrib['dbAccessionId']


# def map_pdb_to_uniprot(pdb_id):
#     pdb_mapping_response = requests.get(
#         pdb_mapping_url, params={'query': pdb_id}
#     ).text
#     uniprot_id = get_uniprot_accession_id(pdb_mapping_response)
#     return uniprot_id


# # PDB seq
# def get_seq_from_PDB():
#     decoded_data = fetch(pdb_id)
#     print(decoded_data.entity_list)
#     for i in decoded_data.entity_list:

#         #빈 문자열이 담기길래 if문 처리 해줌
#         if len(i['sequence']) > 0:
#             seq_pdb.append(i['sequence'])

#     print(seq_pdb)


# #전체 sequence 받기
# def get_seq_from_expasy():
#     with ExPASy.get_sprot_raw(uniprot_id) as handle:
#         seq_record = SeqIO.read(handle, "swiss")
#     seq = str(seq_record.seq)
#     print(seq_record.id)
#     print(seq_record.name)
#     # print(repr(seq_record.seq))
#     # print("Length %i" % len(seq_record))
#     # print(seq_record.annotations["keywords"])
#     return seq
    

#AlphaFold seq
#시간 오래 걸림
def get_seq_from_alphafold():
    base_url = "https://alphafold.ebi.ac.uk/entry/"
    url = base_url+uniprot_id

    driver.get(url)
    print(driver.current_url)
    print(driver.name)

    elems = driver.find_elements(By.CLASS_NAME, "msp-sequence-present")
    seq = ""
    for elem in elems:
        seq += elem.text

    print("found alphafold", seq)
    seq_alphafold = seq
    return seq

#charge 값 selenium으로 구하기
def get_charge(lst1, lst2):
    url = "https://protcalc.sourceforge.net"

    #페이지 열기
    driver.get(url)
    print(driver.current_url)
    print(driver.name)

    
    # WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
    iframe = driver.find_element(By.CSS_SELECTOR, 'body > div > iframe')
    driver.switch_to_frame(iframe)
    # WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sequence"]')))

    for i in lst1:
        driver.find_element(By.XPATH, '/html/body/form/center[2]/textarea').clear()
        driver.find_element(By.XPATH, '//*[@id="sequence"]').send_keys(i)
        driver.find_element(By.XPATH, '/html/body/form/center[6]/table/tbody/tr[1]/td[2]/input[2]')
        driver.find_element(By.XPATH, '/html/body/form/center[7]/input').click()
        time.sleep(5)
        # WebDriverWait(driver, 15).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div/table/tbody/tr[6]/td[2]'))
        #     )
        charge = driver.find_element(By.XPATH, '/html/body/center[3]/h2')
        print(charge.text)
        # common_charge.append(charge.text)
        
    

    for i in lst2:
        driver.find_element(By.XPATH, '//*[@id="sequence"]').clear()
        driver.find_element(By.XPATH, '//*[@id="sequence"]').send_keys(i)
        driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/form/table/tbody/tr[2]/td[5]/input').click()
        time.sleep(2)
        # WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div/table/tbody/tr[6]/td[2]')))
        charge = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/table/tbody/tr[6]/td[2]')
        diff_charge.append(charge.text)


def charge(array):
    seq_pieces_charge = []
    url = "https://protcalc.sourceforge.net"

    #페이지 열기
    driver.get(url)
    print(driver.current_url)
    print(driver.name)

    
    # WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
    # iframe = driver.find_element(By.CSS_SELECTOR, 'body > div > iframe')
    # driver.switch_to.frame(iframe)
    # WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sequence"]')))

    driver.find_element(By.XPATH, '/html/body/form/center[6]/table/tbody/tr[1]/td[2]/input[2]').click() # back으로 페이지 이동하므로 check 상태가 저장되어 있다 -> 처음 한 번만 해줘도 됨
    for i in array:
        driver.find_element(By.XPATH, '/html/body/form/center[2]/textarea').clear()
        driver.find_element(By.XPATH, '/html/body/form/center[2]/textarea').send_keys(i)
        driver.find_element(By.XPATH, '/html/body/form/center[7]/input').click()
        time.sleep(2)
        # WebDriverWait(driver, 15).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div/table/tbody/tr[6]/td[2]'))
        #     )
        charge = driver.find_element(By.XPATH, '/html/body/center[3]/h2')
        charge = charge.text
        charge = charge.split("=")[-1]
        print(charge)

        seq_pieces_charge.append(float(charge))

        driver.back() # 뒤로 돌아가서 seq 입력하기

    
    return seq_pieces_charge
        

def get_domain(uniprotID):
    url = "https://www.uniprot.org/uniprotkb/" + uniprotID + "/entry#family_and_domains"

    #페이지 열기
    driver.get(url)
    print(driver.current_url)
    print(driver.name)

    domain_seq_array = []
    x_axis = ['C_terminus']
    time.sleep(10)
    table = driver.find_element(By.XPATH, '//*[@id="family_and_domains"]/div/div[2]/protvista-manager/div/protvista-datatable/table')
    select = Select(driver.find_element(By.XPATH, '//*[@id="family_and_domains"]/div/div[2]/protvista-manager/div/protvista-datatable/table/thead/tr/th[2]/span/select'))  
    select.select_by_value('Domain')

    count = 0
    domain_flag = False
    for tr in table.find_elements(By.TAG_NAME, 'tr'):
        if domain_flag:
            td = tr.find_element(By.TAG_NAME, "td")
            domain_seq_array.append(td.get_attribute('innerText').strip('Sequence: '))
            count += 1
            x_axis.append('Domain_' + str(count))
            domain_flag = False
            
            continue

        if tr.get_attribute('class') == 'even' or tr.get_attribute('class') == 'odd':
            domain_flag = True

    x_axis.append('N_terminus')
        # for i in range(len(tr)):
        #     if tr_id == tr[i].getAttribute('data-id'):
        #         tr_idx.append(i)

        # td = tr.find_element_by_class_name('find_element_by_class_name') 
    print(domain_seq_array)  
    return  domain_seq_array

#LCS 알고리즘
def lcs(word1, word2):
    max = 0
    index = 0
    letters =[[0 for _ in range(len(word2) + 1)] for _ in range(len(word1) + 1)]

    for i in range(len(word1)):
        for j in range(len(word2)):
            if word1[i] == word2[j]:
                letters[i+1][j+1] = letters[i][j] + 1

            if max < letters[i+1][j+1]:
                max = letters[i+1][j+1]
                index = i + 1

    return index-max, index



def get_cn_terminus(seq, domain_seq_array):
    start1, end1 = lcs(seq, domain_seq_array[0])
    start2, end2 = lcs(seq, domain_seq_array[-1])

    c_terminus_seq = seq[:start1]
    n_terminus_seq = seq[end2:]

    if c_terminus_seq != '':
        print("C_terminus", c_terminus_seq)
    if n_terminus_seq != '':
        print("N_terminus", n_terminus_seq)

    return c_terminus_seq, n_terminus_seq


def concatenate_array(c, n, array):
    seq_array = []
    if c != '':
        seq_array.append(c)

    if n != '':
        array.append(n)

    arr1 = np.array(seq_array)
    arr2 = np.array(array)
    arr = np.concatenate((seq_array, array))

    print(arr)
    return arr



#DB 연결 및 열기
conn = pymysql.connect(host='localhost', user='dev_kyome', password='password', database='protein_sequence', port=3307)
cur = conn.cursor()

df = pd.read_csv('Human protein atlas-brain/brain_category_rna_amygdala_Detected.tsv', sep = '\t')
uniprot_id_array = df['Uniprot'].dropna().to_list()
print(uniprot_id_array)

# uniprot_id_array = ['P17600']

# print(uniprot_id_array)
# uniprot_id_array = uniprot_column.values
# print(uniprot_id_array)

# uniprot_id_array = ['P05067', 'P05049', 'P43014']

for i in uniprot_id_array:
    uniprot_id = i
    #seq 정보, charge값 구하기
    try:
        seq_alphafold = get_seq_from_alphafold() #AlphaFold에서 구한 seq(C + Domain + N)
        domain_result = get_domain(uniprot_id) #Domain별로 구분된 array
        c_terminus_seq, n_terminus_seq = get_cn_terminus(seq_alphafold, domain_result) #C & N terminus seq
        array_complete = concatenate_array(c_terminus_seq, n_terminus_seq, domain_result) #C & Domain & N seq 전부
        seq_pieces_charge = charge(array_complete) #전체 seq의 charge값
        print(seq_pieces_charge)

        # array stringify
        test = "test"
        array_complete_str = ' '.join(array_complete)
        x_axis_str = ' '.join(x_axis)
        seq_pieces_charge_str = ' '.join(map(str,seq_pieces_charge))

        print(array_complete_str, x_axis_str, seq_pieces_charge_str)


        # if (conn.is_connected()):
        #     print("Connected")
        # else:
        #     print("Not connected")
            
        
        cur.execute('INSERT INTO charge_info (uniprotID, sequence, position, charge) VALUES (%s, %s, %s, %s)', (uniprot_id, array_complete_str, x_axis_str, seq_pieces_charge_str))
        conn.commit()


    # 그래프 그리기
    # plt.plot(x_axis, seq_pieces_charge, '-bo')
    # plt.show()
    # print(mpld3.fig_to_html(f, figid='THIS_IS_FIGID'))

    except:
        print("에러 발생: " + uniprot_id)
        error_id_array.append(uniprot_id)

conn.close()

print(error_id_array, str(len(error_id_array)) + "개")




