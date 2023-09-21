import streamlit as st
import numpy as np
import pandas as pd
from stmol import showmol,render_pdb,render_pdb_resn
import py3Dmol
import mysql.connector
from sshtunnel import SSHTunnelForwarder
import paramiko
import pymysql

# SSH tunnel parameters
ssh_host = "164.125.254.141"
ssh_port = 4001
ssh_username = "shlee"
ssh_password = "korea2020"

# MySQL database connection parameters
db_host = "127.0.0.1"
db_port = 3306
db_user = "root"
db_password = "password"
db_name = "protein_sequence"

# Create an SSH client and establish a tunnel
try:
    with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        remote_bind_address=(db_host, db_port)
    ) as tunnel:
        st.success("SSH tunnel established successfully.")

        conn = pymysql.connect(
            host='127.0.0.1', 
            user=db_user,
            passwd=db_password, 
            db=db_name,
            port=tunnel.local_bind_port,
            connect_timeout=180)
        print(conn)

except Exception as e:
    st.error(f"Error establishing SSH tunnel or connecting to MySQL: {e}")

    

if conn:

    st.title('Protein Sequence')
    st.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.') # df, err, func, keras!

    st.header('Uniprot ID')
    user_input = st.text_input(
        label="Enter the Uniprot ID",
        max_chars=100,
        key="my_text_input"
    )

    if user_input:
        # condition = "uniprot_id = '" + user_input + "'"
        # query = f"SELECT position, charge FROM charge_info WHERE {condition}"
        query = "SELECT position, charge FROM charge_info WHERE uniprot_id = 'A0A556C1E4'"

        try:
            print(conn)
            with conn.cursor() as cursor:
                cursor.execute(query)
                selected_row = cursor.fetchall()
        except pymysql.MySQLError as err:
            print(err)
            st.error(f"Error executing the query: {err}")

        # if selected_row:
        #     st.table(selected_row)
        # else:
        #     st.warning("No data found based on the specified condition.")



    st.header('Charge info')
    chart_data_n = pd.DataFrame({
        'position':["C_terminus", "Domain_1", "Domain_2", "N_terminus"],
        'charge': [3.9, -2.1, 9.3, 1.9]
    })
    chart_data_n = chart_data_n.rename(columns={'position':'index'}).set_index('index')
    st.bar_chart(chart_data_n)

    st.header('Protein Image')

    # 1A2C
    # Structure of thrombin inhibited by AERUGINOSIN298-A from a BLUE-GREEN ALGA
    xyzview = py3Dmol.view(query='pdb:1A2C') 
    xyzview.setStyle({'cartoon':{'color':'spectrum'}})
    showmol(render_pdb_resn(viewer = render_pdb(id = '1A2C'),resn_lst = ['ALA',]))

# st.image('./AF-A0A6H5IF59-F1.png')



# st.text('Fixed width text')
# st.markdown('_Markdown_') # see *
# st.caption('Balloons. Hundreds of them...')
# st.latex(r''' e^{i\pi} + 1 = 0 ''')
# st.write(['st', 'is <', 3]) # see *
# st.title('My title')
# st.header('My header')
# st.subheader('My sub')
# st.code('for i in range(8): foo()')

