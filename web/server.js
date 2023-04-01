const mysql = require('mysql');  // mysql 모듈 로드
const http = require('http')
const express = require('express');
const { expressTest } = require('./expressTest')

const app = express();
app.use( express.json());

app.get()

app.listen(3000, () => {
    console.log('3000번 포트에서 요청 대기중...');
})


const conn = {  // mysql 접속 설정
    host: 'localhost',
    port: '3307',
    user: 'dev_kyome',
    password: 'password',
    database: 'protein_sequence'
};


let connection = mysql.createConnection(conn); // DB 커넥션 생성
connection.connect();   // DB 접속

let sql = "select * from charge_info";

connection.query(sql, function (err, results, fields) {
    if (err) {
        console.log(err);
    }
    console.log(results);
});
