const mysql = require('mysql');  // mysql 모듈 로드
const express = require('express');

const conn = {  // mysql 접속 설정
    host: 'localhost',
    port: '3307',
    user: 'dev_kyome',
    password: 'password',
    database: 'protein_sequence'
};

var app = express();

let connection = mysql.createConnection(conn); // DB 커넥션 생성
connection.connect();   // DB 접속

let sql = "select * from charge_info";

connection.query(sql, function (err, results, fields) {
    if (err) {
        console.log(err);
    }
    console.log(results);
});
