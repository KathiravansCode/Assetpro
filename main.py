from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from PIL import Image
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
from werkzeug.utils import secure_filename
from flask import send_file
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import threading
import time
import shutil
import hashlib
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser

#pip install pycryptodome --user
from Crypto import Random
from Crypto.Cipher import AES

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="cloud_brain_py"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####

class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
    
@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""
    mycursor = mydb.cursor()
    now = date.today() #datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    #######################
    #ky="abc123"
    #obj=AESCipher(ky)

    '''mycursor.execute("SELECT * FROM vb_document where id=3")
    dtt = mycursor.fetchone()
    emsg=dtt[3]
    
    enc=emsg.encode("utf-8")
    dec=obj.decrypt(enc)
    print(dec)'''

    '''v="my documents"
    v1=obj.encrypt(v)
    sql="insert into vb_document(id,title) values(%s,%s)"
    val=(3,v1)
    mycursor.execute(sql,val)
    mydb.commit()'''
    ######################
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        rd = request.form['rd']
        
        mycursor.execute("SELECT count(*) FROM vb_register where uname=%s",(username1,))
        myresult = mycursor.fetchone()[0]
        
        if myresult>0:
            mycursor.execute("SELECT * FROM vb_register where uname=%s",(username1,))
            rr = mycursor.fetchone()

            ky=username1
            obj=AESCipher(ky)
        
            pw=obj.decrypt(rr[35].encode("utf-8"))
            if pw==password1:
                session['username'] = username1
                fu=open("user.txt","w")
                fu.write(username1)
                fu.close()
                result=" Your Logged in sucessfully**"

                
                rdd=obj.encrypt(rd)
                mycursor.execute("update vb_register set last_date=%s,status=0 where uname=%s",(rdd,username1))
                mydb.commit()
    
                return redirect(url_for('user_home'))
            else:
                msg="Invalid Username or Password!"
                
                
        else:
            mycursor.execute("SELECT * FROM vb_user where userid=%s",(username1,))
            rr2 = mycursor.fetchone()
            ky=rr2[1]
            obj=AESCipher(ky)
            pw=obj.decrypt(rr2[6].encode("utf-8"))
            
            if pw==password1:
                session['username'] = rr2[1]
                return redirect(url_for('user_home'))
            else:
                msg="Invalid Username or Password!"
       

    return render_template('index.html',msg=msg,act=act,rdate=rdate)

@app.route('/login',methods=['POST','GET'])
def login():
    cnt=0
    act=""
    msg=""
    mycursor = mydb.cursor()
    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        
        
        mycursor.execute("SELECT count(*) FROM vb_relative where mobile=%s",(username1,))
        myresult = mycursor.fetchone()[0]
        
        if myresult>0:
            mycursor.execute("SELECT * FROM vb_relative where mobile=%s",(username1,))
            rr = mycursor.fetchone()

            ky=rr[1]
            obj=AESCipher(ky)
        
            pw=obj.decrypt(rr[6].encode("utf-8"))
            if pw==password1:
                session['username'] = username1
                
                session['rid'] = rr[0]
                return redirect(url_for('home'))
            else:
                msg="Invalid Username or Password!"
                
        else:
            msg="Invalid Username or Password!"
   

    return render_template('login.html',msg=msg,act=act)

@app.route('/send_alert',methods=['POST','GET'])
def send_alert():
    msg=""
    act=request.args.get("act")
    ldate=""
    days=0
    mess=""
    email=""
    ss=""
    alert_st=""

    ff=open("uu.txt","r")
    un=ff.read()
    ff.close()

    if un is None:
        mycursor.execute("SELECT * FROM vb_register order by id limit 0,1")
        ud = mycursor.fetchone()
        un=ud[34]
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(un,))
    rr1 = mycursor.fetchone()

    now = date.today() #datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    #for rr1 in rr:
    un=rr1[34]
    alert=rr1[42]
    if alert==0:
        alert_st="1"
    ky=un
    obj=AESCipher(ky)

    ldate=obj.decrypt(rr1[36].encode("utf-8"))
    st=rr1[39]
    mobile=obj.decrypt(rr1[12].encode("utf-8"))
    email=obj.decrypt(rr1[11].encode("utf-8"))

    ld=ldate.split('-')
    rd=rdate.split('-')

    l1=int(ld[2])
    l2=int(ld[1])
    l3=int(ld[0])

    r1=int(rd[2])
    r2=int(rd[1])
    r3=int(rd[0])

    d0 = date(l1, l2, l3)
    d1 = date(r1, r2, r3)
    delta = d1 - d0
    days=delta.days
    print(delta.days)

    if days>=45:
        if st==3:
            a=""
        else:
            ss="1"
            mycursor.execute("update vb_register set status=3 where uname=%s",(un,))
            mydb.commit()
            mess="User("+un+") has does not access the application in last 45 days, update the status of the user or access the account"

            mycursor.execute("SELECT * FROM vb_user where uname=%s",(un,))
            d1 = mycursor.fetchone()
            email=obj.decrypt(d1[4].encode("utf-8"))
            print(mess)
            print(email)
    elif days>=30:

        if st==2:
            a=""
        else:
            ss="1"
            mycursor.execute("update vb_register set status=2 where uname=%s",(un,))
            mydb.commit()
            mess="Dear "+un+", From:Cloud Brain, You are not access your account in last 30 days, so you want to access your account"
            print(mess)
            print(email)
    elif days>=15:

        if st==1:
            a=""
        else:
            ss="1"
            mycursor.execute("update vb_register set status=1 where uname=%s",(un,))
            mydb.commit()
            mess="Dear "+un+", From:Cloud Brain, You are not access your account in last 15 days, so you want to access your account"
            print(mess)
            print(email)


    print(mess)
    print(email) 

        
        

    return render_template('send_alert.html',msg=msg,act=act,ldate=ldate,days=days,mess=mess,email=email,ss=ss,alert_st=alert_st)

@app.route('/date_update', methods=['GET', 'POST'])
def date_update():
    msg=""
    act=""
    uname=""
    users=""
    ldate=""
    us=""
    if 'username' in session:
        uname = session['username']

    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register")
    ud = mycursor.fetchall()

    if request.method=='POST':
        users=request.form['users']
        if users=="":
            s="1"
        else:
            print(users)
            mycursor.execute("SELECT * FROM vb_register where uname=%s",(users,))
            ud2 = mycursor.fetchone()
            ky=users
            obj=AESCipher(ky)

            #fname=ud2[1]            
            #fg=obj.decrypt(fname.encode("utf-8"))
            #print(fg)
            
            ldate=obj.decrypt(ud2[36].encode("utf-8"))
            print(ldate)

            us=request.form['us']
        if us=="":
            s="1"
        else:
            
            ky=us
            obj=AESCipher(ky)
            last_date=request.form['last_date']
            ldd=obj.encrypt(last_date)
            mycursor.execute("update vb_register set last_date=%s where uname=%s",(ldd,us))
            mydb.commit()
            users=us

            ff=open("uu.txt","w")
            un=ff.write(us)
            ff.close()
    
            msg="ok"
            #return redirect(url_for('date_update')) 

    return render_template('date_update.html',msg=msg,ud=ud,users=users,ldate=ldate,us=us)

#######
##ABE – Attribute Based Encryption
def AC17CPABE(ABEnc):
   # def __init__(self, group_obj, assump_size, verbose=False):
    ABEnc.__init__(self)
    self.group = group_obj
    self.assump_size = assump_size  # size of linear assumption, at least 2
    self.util = MSP(self.group, verbose)
    def setup(self):
        """
        Generates public key and master secret key.
        """
        if debug:
            print('\nSetup algorithm:\n')

        # generate two instances of the k-linear assumption
        A = []
        B = []
        for i in range(self.assump_size):
            A.append(self.group.random(ZR))
            B.append(self.group.random(ZR))  # note that A, B are vectors here
        # vector
        k = []
        for i in range(self.assump_size + 1):
            k.append(self.group.random(ZR))
        # pick a random element from the two source groups and pair them
        g = self.group.random(G1)
        h = self.group.random(G2)
        e_gh = pair(g, h)
        # now compute various parts of the public parameters

        # compute the [A]_2 term
        h_A = []
        for i in range(self.assump_size):
            h_A.append(h ** A[i])
        h_A.append(h)
        # compute the e([k]_1, [A]_2) term
        g_k = []
        for i in range(self.assump_size + 1):
            g_k.append(g ** k[i])
        e_gh_kA = []
        for i in range(self.assump_size):
            e_gh_kA.append(e_gh ** (k[i] * A[i] + k[self.assump_size]))
        # the public key
        pk = {'h_A': h_A, 'e_gh_kA': e_gh_kA}
        # the master secret key
        msk = {'g': g, 'h': h, 'g_k': g_k, 'A': A, 'B': B}
        return pk, msk
    def keygen(self, pk, msk, attr_list):
        if debug:
            print('\nKey generation algorithm:\n')
        # pick randomness
        r = []
        sum = 0
        for i in range(self.assump_size):
            rand = self.group.random(ZR)
            r.append(rand)
            sum += rand
        # compute the [Br]_2 term
        # first compute just Br as it will be used later too
        Br = []
        for i in range(self.assump_size):
            Br.append(msk['B'][i] * r[i])
        Br.append(sum)
        # now compute [Br]_2
        K_0 = []
        for i in range(self.assump_size + 1):
            K_0.append(msk['h'] ** Br[i])

    def encrypt(self, pk, msg, policy_str):
        if debug:
            print('\nEncryption algorithm:\n')
        policy = self.util.createPolicy(policy_str)
        mono_span_prog = self.util.convert_policy_to_msp(policy)
        num_cols = self.util.len_longest_row
        # pick randomness
        s = []
        sum = 0
        for i in range(self.assump_size):
            rand = self.group.random(ZR)
            s.append(rand)
            sum += rand
        # compute the e(g, h)^(k^T As) . m term
        Cp = 1
        for i in range(self.assump_size):
            Cp = Cp * (pk['e_gh_kA'][i] ** s[i])
        Cp = Cp * msg
        return {'policy': policy, 'C_0': C_0, 'C': C, 'Cp': Cp}

    def decrypt(self, pk, ctxt, key):
        if debug:
            print('\nDecryption algorithm:\n')
        nodes = self.util.prune(ctxt['policy'], key['attr_list'])
        if not nodes:
            print ("Policy not satisfied.")
            return None
        prod1_GT = 1
        prod2_GT = 1
        for i in range(self.assump_size + 1):
            prod_H = 1
            prod_G = 1
            for node in nodes:
                attr = node.getAttributeAndIndex()
                attr_stripped = self.util.strip_index(attr)  # no need, re-use not allowed
                # prod_H *= key['K'][attr_stripped][i] ** coeff[attr]
                # prod_G *= ctxt['C'][attr][i] ** coeff[attr]
                prod_H *= key['K'][attr_stripped][i]
                prod_G *= ctxt['C'][attr][i]
            prod1_GT *= pair(key['Kp'][i] * prod_H, ctxt['C_0'][i])
            prod2_GT *= pair(prod_G, key['K_0'][i])
        return ctxt['Cp'] * prod2_GT / prod1_GT


###########
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()

    now = date.today() #datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    if request.method=='POST':
        fname=request.form['fname']
        lname=request.form['lname']
        gender=request.form['gender']
        dob=request.form['dob']
        address=request.form['address']
        address2=request.form['address2']
        pincode=request.form['pincode']
        city=request.form['city']
        state=request.form['state']
        country=request.form['country']
        email=request.form['email']
        mobile=request.form['mobile']
        mobile2=request.form['mobile2']
        landline=request.form['landline']
        adhar=request.form['adhar']
        voter=request.form['voter']
        pancard=request.form['pancard']
        driving=request.form['driving']
        uname=request.form['uname']
        pass1=request.form['pass']

        ky=uname
        obj=AESCipher(ky)
        
        fname1=obj.encrypt(fname)
        lname1=obj.encrypt(lname)
        gender1=obj.encrypt(gender)
        dob1=obj.encrypt(dob)
        address1=obj.encrypt(address)
        address21=obj.encrypt(address2)
        pincode1=obj.encrypt(pincode)
        city1=obj.encrypt(city)
        state1=obj.encrypt(state)
        country1=obj.encrypt(country)
        email1=obj.encrypt(email)
        mobile1=obj.encrypt(mobile)
        mobile21=obj.encrypt(mobile2)
        landline1=obj.encrypt(landline)
        adhar1=obj.encrypt(adhar)
        voter1=obj.encrypt(voter)
        pancard1=obj.encrypt(pancard)
        driving1=obj.encrypt(driving)
        pass11=obj.encrypt(pass1)
        rdate1=obj.encrypt(rdate)        

        mycursor.execute("SELECT count(*) FROM vb_register where uname=%s",(uname,))
        myresult = mycursor.fetchone()[0]

        if myresult==0:
        
            mycursor.execute("SELECT max(id)+1 FROM vb_register")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            sql = "INSERT INTO vb_register(id,fname,lname,gender,dob,address,address2,pincode,city,state,country,email,mobile,mobile2,landline,adhar,voter,pancard,driving,uname,pass,rdate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,fname1,lname1,gender1,dob1,address1,address21,pincode1,city1,state1,country1,email1,mobile1,mobile21,landline1,adhar1,voter1,pancard1,driving1,uname,pass11,rdate1)
            mycursor.execute(sql, val)
            mydb.commit()

            
            print(mycursor.rowcount, "Registered Success")
            msg="success"
            
            #if cursor.rowcount==1:
            #    return redirect(url_for('index',act='1'))
        else:
            
            msg='fail'
            
    
    return render_template('register.html', msg=msg)

@app.route('/user_home', methods=['GET', 'POST'])
def user_home():
    msg=""
    act=""
    uname=""
    rname=""
    data=[]
    if 'username' in session:
        uname = session['username']
    print(uname)
    ky=uname
    obj=AESCipher(ky)
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
   
    #fname=obj.decrypt(dat[1].encode("utf-8"))
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    data.append(obj.decrypt(dat[3].encode("utf-8")))
    data.append(obj.decrypt(dat[4].encode("utf-8")))
    data.append(obj.decrypt(dat[5].encode("utf-8")))
    data.append(obj.decrypt(dat[6].encode("utf-8")))
    data.append(obj.decrypt(dat[7].encode("utf-8")))
    data.append(obj.decrypt(dat[8].encode("utf-8")))
    data.append(obj.decrypt(dat[9].encode("utf-8")))
    data.append(obj.decrypt(dat[10].encode("utf-8")))
    data.append(obj.decrypt(dat[11].encode("utf-8")))
    data.append(obj.decrypt(dat[12].encode("utf-8")))
    data.append(obj.decrypt(dat[13].encode("utf-8")))
    data.append(obj.decrypt(dat[14].encode("utf-8")))
    data.append(obj.decrypt(dat[15].encode("utf-8")))
    data.append(obj.decrypt(dat[16].encode("utf-8")))
    data.append(obj.decrypt(dat[17].encode("utf-8")))
    data.append(obj.decrypt(dat[18].encode("utf-8")))

    if dat[19]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[19].encode("utf-8")))

    if dat[20]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[20].encode("utf-8")))
        
    if dat[21]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[21].encode("utf-8")))

    if dat[22]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[22].encode("utf-8")))

    if dat[23]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[23].encode("utf-8")))

    if dat[24]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[24].encode("utf-8")))

    if dat[25]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[25].encode("utf-8")))

    if dat[26]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[26].encode("utf-8")))

    if dat[27]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[27].encode("utf-8")))

    if dat[28]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[28].encode("utf-8")))

    if dat[29]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[29].encode("utf-8")))

    if dat[30]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[30].encode("utf-8")))

    if dat[31]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[31].encode("utf-8")))

    if dat[32]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[32].encode("utf-8")))

    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    data.append(dat[34])
    data.append(obj.decrypt(dat[35].encode("utf-8")))
    if dat[36]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[36].encode("utf-8")))
    data.append(dat[37])
    data.append(dat[38])
    data.append(dat[39])
    data.append(dat[40])
    data.append(obj.decrypt(dat[41].encode("utf-8")))
    data.append(dat[42])
    data.append(dat[43])
    
    if data[40]==0:
        rname=""
    else:
        mycursor.execute("SELECT * FROM vb_relative where id=%s",(data[40], ))
        r2 = mycursor.fetchone()
        rname=obj.decrypt(r2[2].encode("utf-8"))
                

    return render_template('user_home.html',data=data,act=act,rname=rname,uname=uname)

@app.route('/relative', methods=['GET', 'POST'])
def relative():
    msg=""
    act=request.args.get("act")
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    if request.method=='POST':
        name=request.form['name']
        relation=request.form['relation']
        mobile=request.form['mobile']
        email=request.form['email']

        rn=randint(100,999)
                
        mycursor.execute("SELECT max(id)+1 FROM vb_relative")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        pw=str(maxid)+str(rn)
        pw1=obj.encrypt(pw)
        
        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        rdate1=obj.encrypt(rdate)

        if name=="":
            name1=""
        else:
            name1=obj.encrypt(name)
        if relation=="":
            relation1=""
        else:
            relation1=obj.encrypt(relation)
        if mobile=="":
            mobile1=""
        else:
            mobile1=mobile
        if email=="":
            email1=""
        else:
            email1=obj.encrypt(email)
        
        sql = "INSERT INTO vb_relative(id,uname,name,relation,mobile,email,pass,rdate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,name1,relation1,mobile1,email1,pw1,rdate1)
        mycursor.execute(sql, val)
        mydb.commit()
 
        print(mycursor.rowcount, "Registered Success")
        msg="success"

    mycursor.execute("SELECT count(*) FROM vb_relative where uname=%s",(uname, ))
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        st="1"
        mycursor.execute("SELECT * FROM vb_relative where uname=%s",(uname, ))
        dd = mycursor.fetchall()
        for rr in dd:
            dt=[]
            
            dt.append(rr[0])
            dt.append(rr[1])
            if rr[2]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[2].encode("utf-8")))
            if rr[3]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[3].encode("utf-8")))
            if rr[4]=="":
                dt.append("")
            else:
                dt.append(rr[4])
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[5].encode("utf-8")))
            

            data2.append(dt)
            
    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from vb_relative where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('relative'))

    return render_template('relative.html',msg=msg,data=data,data2=data2,act=act,st=st,uname=uname)

@app.route('/ac_email', methods=['GET', 'POST'])
def ac_email():
    msg=""
    act=request.args.get("act")
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']
    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    if request.method=='POST':
        email=request.form['email']
        pass1=request.form['pass']
        
        if email=="":
            email1=""
        else:
            email1=obj.encrypt(email)

        if pass1=="":
            pass11=""
        else:
            pass11=obj.encrypt(pass1)
        mycursor.execute("SELECT max(id)+1 FROM vb_email")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        rdate1=obj.encrypt(rdate)
        
        sql = "INSERT INTO vb_email(id,uname,email,pass,rdate) VALUES (%s,%s,%s,%s,%s)"
        val = (maxid,uname,email1,pass11,rdate1)
        mycursor.execute(sql, val)
        mydb.commit()
 
        print(mycursor.rowcount, "Registered Success")
        msg="success"

    mycursor.execute("SELECT count(*) FROM vb_email where uname=%s",(uname, ))
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        st="1"
        mycursor.execute("SELECT * FROM vb_email where uname=%s",(uname, ))
        dd = mycursor.fetchall()
        for rr in dd:
            dt=[]
            dt.append(rr[0])
            dt.append(rr[1])
            dt.append(rr[2])
            
            if rr[3]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[3].encode("utf-8")))
            if rr[4]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[4].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[5].encode("utf-8")))

            na=""
            if rr[1]==0:
                na=""
            else:
                mycursor.execute("SELECT * FROM vb_relative where id=%s",(rr[1], ))
                r2 = mycursor.fetchone()
                na=obj.decrypt(r2[2].encode("utf-8"))

            dt.append(na)
            data2.append(dt)
            
        


    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from vb_email where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('ac_email'))

    return render_template('ac_email.html',msg=msg,data=data,data2=data2,act=act,st=st,uname=uname)


@app.route('/account', methods=['GET', 'POST'])
def account():
    msg=""
    act=request.args.get("act")
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']
    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    if request.method=='POST':
        bank=request.form['bank']
        branch=request.form['branch']
        account=request.form['account']
        pinno=request.form['pinno']
        cardno=request.form['cardno']
        acpass=request.form['acpass']
        

        mycursor.execute("SELECT max(id)+1 FROM vb_account")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        rdate1=obj.encrypt(rdate)
        if bank=="":
            bank1=""
        else:
            bank1=obj.encrypt(bank)

        if branch=="":
            branch1=""
        else:
            branch1=obj.encrypt(branch)

        if account=="":
            account1=""
        else:
            account1=obj.encrypt(account)
        if pinno=="":
            pinno1=""
        else:
            pinno1=obj.encrypt(pinno)
        if cardno=="":
            cardno1=""
        else:
            cardno1=obj.encrypt(cardno)
        if acpass=="":
            acpass1=""
        else:
            acpass1=obj.encrypt(acpass)
        
        sql = "INSERT INTO vb_account(id,uname,bank,branch,account,pinno,cardno,acpass,rdate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,bank1,branch1,account1,pinno1,cardno1,acpass1,rdate1)
        mycursor.execute(sql, val)
        mydb.commit()
 
        print(mycursor.rowcount, "Registered Success")
        msg="success"

    mycursor.execute("SELECT count(*) FROM vb_account where uname=%s",(uname, ))
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        st="1"
        mycursor.execute("SELECT * FROM vb_account where uname=%s",(uname, ))
        dd = mycursor.fetchall()
        for rr in dd:
            dt=[]
            dt.append(rr[0])
            dt.append(rr[1])
            dt.append(rr[2])
            
            if rr[3]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[3].encode("utf-8")))
            if rr[4]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[4].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[5].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[6].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[7].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[8].encode("utf-8")))
            

            na=""
            if rr[1]==0:
                na=""
            else:
                mycursor.execute("SELECT * FROM vb_relative where id=%s",(rr[1], ))
                r2 = mycursor.fetchone()
                na=obj.decrypt(r2[2].encode("utf-8"))

            dt.append(na)
            data2.append(dt)
            
        


    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from vb_account where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('account'))

    return render_template('account.html',msg=msg,data=data,data2=data2,act=act,st=st,uname=uname)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    msg=""
    msg1=""
    act=request.args.get("act")
    uname=""
    st=""
    email=""
    mess=""
    data2=[]
    if 'username' in session:
        uname = session['username']
    fu=open("user.txt","r")
    uname=fu.read()
    fu.close()
    
    ky=uname
    obj=AESCipher(ky)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        userid=request.form['userid']
        pass1=request.form['pass']
    
        mycursor.execute("SELECT count(*) FROM vb_user where userid=%s",(userid,))
        cnt = mycursor.fetchone()[0]
        if cnt==0:

            mycursor.execute("SELECT max(id)+1 FROM vb_user")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            rdate1=obj.encrypt(rdate)

            rn1=randint(10000,99999)
            #str(rn1)
            

            if name=="":
                name1=""
            else:
                name1=obj.encrypt(name)

            if mobile=="":
                mobile1=""
            else:
                mobile1=obj.encrypt(mobile)

            if email=="":
                email1=""
            else:
                email1=obj.encrypt(email)
            if pass1=="":
                pass11=""
            else:
                pass11=obj.encrypt(pass1)
            
            sql = "INSERT INTO vb_user(id,uname,name,mobile,email,userid,pass,rdate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,uname,name1,mobile1,email1,userid,pass11,rdate1)
            mycursor.execute(sql, val)
            mydb.commit()
     
            print(mycursor.rowcount, "Registered Success")
            msg1="success"
            mess="Dear "+name+", Sub User ID: "+userid+", Password: "+pass1+", by "+uname;
            print(mess)
        else:
            msg="Already Exist!"

    mycursor.execute("SELECT count(*) FROM vb_user where uname=%s",(uname, ))
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        st="1"
        mycursor.execute("SELECT * FROM vb_user where uname=%s",(uname, ))
        dd = mycursor.fetchall()
        for rr in dd:
            dt=[]
            dt.append(rr[0])
            dt.append(rr[1])
            if rr[2]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[2].encode("utf-8")))
            if rr[3]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[3].encode("utf-8")))
            if rr[4]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[4].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(rr[5])
            if rr[6]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[6].encode("utf-8")))
            if rr[7]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[7].encode("utf-8")))
            
            data2.append(dt)
            
        


    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from vb_user where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_user'))

    return render_template('add_user.html',msg=msg,msg1=msg1,data=data,data2=data2,act=act,st=st,uname=uname,email=email,mess=mess)

@app.route('/audio', methods=['GET', 'POST'])
def audio():
    msg=""
    act=request.args.get("act")
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']
    ky=uname
    obj=AESCipher(ky)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    if request.method=='POST':
        ftype=request.form['ftype']
        title=request.form['title']
        details=request.form['details']
        file = request.files['file']
        fname = file.filename
        filename = secure_filename(fname)
        file.save(os.path.join("static/audio", filename))
        ##encryption
        password_provided = ky # This is input in the form of a string
        password = password_provided.encode() # Convert to type bytes
        salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))

        input_file = 'static/audio/'+filename
        output_file = 'static/audio/'+filename
        with open(input_file, 'rb') as f:
            dataa = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(dataa)

        with open(output_file, 'wb') as f:
            f.write(encrypted)
        ###
        filename1=obj.encrypt(filename)
        if ftype=="":
            ftype1=""
        else:
            ftype1=obj.encrypt(ftype) 
        if title=="":
            title1=""
        else:
            title1=obj.encrypt(title)
        if details=="":
            details1=""
        else:
            details1=obj.encrypt(details)

        mycursor.execute("SELECT max(id)+1 FROM vb_audio")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        
        sql = "INSERT INTO vb_audio(id,uname,ftype,title,details,filename,rdate) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,ftype1,title1,details1,filename1,rdate)
        mycursor.execute(sql, val)
        mydb.commit()
 
        print(mycursor.rowcount, "Registered Success")
        msg="success"

    mycursor.execute("SELECT count(*) FROM vb_audio where uname=%s",(uname, ))
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        st="1"
        mycursor.execute("SELECT * FROM vb_audio where uname=%s",(uname, ))
        dd = mycursor.fetchall()
        for rr in dd:
            dt=[]
            dt.append(rr[0])
            dt.append(rr[1])
            dt.append(rr[2])
            if rr[3]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[3].encode("utf-8")))
            if rr[4]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[4].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[5].encode("utf-8")))
            if rr[6]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[6].encode("utf-8")))
            

            na=""
            if rr[1]==0:
                na=""
            else:
                mycursor.execute("SELECT * FROM vb_relative where id=%s",(rr[1], ))
                r2 = mycursor.fetchone()
                na=obj.decrypt(r2[2].encode("utf-8"))

            dt.append(na)
            data2.append(dt)
            
    if act=="down":
        fid=request.args.get("fid")
        mycursor.execute("SELECT * FROM vb_audio where id=%s",(fid, ))
        r3 = mycursor.fetchone()
        fname=obj.decrypt(r3[6].encode("utf-8"))
        ##
        password_provided = ky # This is input in the form of a string
        password = password_provided.encode() # Convert to type bytes
        salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        input_file = 'static/audio/'+fname
        output_file = 'static/down/'+fname
        with open(input_file, 'rb') as f:
            dataa = f.read()

        fernet = Fernet(key)
        encrypted = fernet.decrypt(dataa)

        with open(output_file, 'wb') as f:
            f.write(encrypted)
        ##
        return redirect(url_for('down',fname=fname)) 


    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from vb_audio where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('audio'))

    return render_template('audio.html',msg=msg,data=data,data2=data2,act=act,st=st,uname=uname)




@app.route('/document', methods=['GET', 'POST'])
def document():
    msg=""
    act=request.args.get("act")
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    if request.method=='POST':
        
        title=request.form['title']
        details=request.form['details']
        file = request.files['file']
        fname = file.filename
        filename = secure_filename(fname)
        file.save(os.path.join("static/document", filename))
        ###
        ##encryption
        password_provided = ky # This is input in the form of a string
        password = password_provided.encode() # Convert to type bytes
        salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))

        input_file = 'static/document/'+filename
        output_file = 'static/document/'+filename
        with open(input_file, 'rb') as f:
            dataa = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(dataa)

        with open(output_file, 'wb') as f:
            f.write(encrypted)
        ###
        filename1=obj.encrypt(filename)
            
        if title=="":
            title1=""
        else:
            title1=obj.encrypt(title)
        if details=="":
            details1=""
        else:
            details1=obj.encrypt(details)
        

        mycursor.execute("SELECT max(id)+1 FROM vb_document")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        
        sql = "INSERT INTO vb_document(id,uname,title,details,filename,rdate) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,title1,details1,filename1,rdate)
        mycursor.execute(sql, val)
        mydb.commit()
 
        print(mycursor.rowcount, "Registered Success")
        msg="success"

    mycursor.execute("SELECT count(*) FROM vb_document where uname=%s",(uname, ))
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        st="1"
        mycursor.execute("SELECT * FROM vb_document where uname=%s",(uname, ))
        dd = mycursor.fetchall()
        for rr in dd:
            dt=[]
            dt.append(rr[0])
            dt.append(rr[1])
            dt.append(rr[2])
            if rr[3]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[3].encode("utf-8")))
            if rr[4]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[4].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[5].encode("utf-8")))
           
           

            na=""
            if rr[1]==0:
                na=""
            else:
                mycursor.execute("SELECT * FROM vb_relative where id=%s",(rr[1], ))
                r2 = mycursor.fetchone()
                na=obj.decrypt(r2[2].encode("utf-8"))

            dt.append(na)
            data2.append(dt)
            
        


    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from vb_document where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('document'))

    if act=="down":
        fid=request.args.get("fid")
        mycursor.execute("SELECT * FROM vb_document where id=%s",(fid, ))
        r3 = mycursor.fetchone()
        fname=obj.decrypt(r3[5].encode("utf-8"))
        ##
        password_provided = uname # This is input in the form of a string
        password = password_provided.encode() # Convert to type bytes
        salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        input_file = 'static/document/'+fname
        output_file = 'static/down/'+fname
        with open(input_file, 'rb') as f:
            dataa = f.read()

        fernet = Fernet(key)
        encrypted = fernet.decrypt(dataa)

        with open(output_file, 'wb') as f:
            f.write(encrypted)
        ##
        return redirect(url_for('down',fname=fname))

    return render_template('document.html',msg=msg,data=data,data2=data2,act=act,st=st,uname=uname)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    msg=""
    act=""
    uname=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    mycursor.execute("SELECT * FROM vb_relative where uname=%s",(uname, ))
    dat3 = mycursor.fetchall()
    data3=[]
    for rs3 in dat3:
        dt3=[]
        dt3.append(rs3[0])
        dt3.append(rs3[1])
        dt3.append(obj.decrypt(rs3[2].encode("utf-8")))
        data3.append(dt3)
        

    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dd = mycursor.fetchone()

    if dd[5]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[5].encode("utf-8")))
    if dd[6]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[6].encode("utf-8")))
    if dd[7]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[7].encode("utf-8")))
    if dd[8]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[8].encode("utf-8")))
    if dd[9]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[9].encode("utf-8")))
    if dd[10]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[10].encode("utf-8")))
    if dd[11]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[11].encode("utf-8")))
    if dd[12]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[12].encode("utf-8")))
    if dd[13]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[13].encode("utf-8")))
    if dd[14]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[14].encode("utf-8")))
    if dd[15]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[15].encode("utf-8")))
    if dd[16]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[16].encode("utf-8")))
    if dd[17]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[17].encode("utf-8")))
    if dd[18]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[18].encode("utf-8")))

    data2.append(dd[40])
    

    if request.method=='POST':
        address=request.form['address']
        address2=request.form['address2']
        pincode=request.form['pincode']
        city=request.form['city']
        state=request.form['state']
        country=request.form['country']
        email=request.form['email']
        mobile=request.form['mobile']
        mobile2=request.form['mobile2']
        landline=request.form['landline']
        adhar=request.form['adhar']
        voter=request.form['voter']
        pancard=request.form['pancard']
        driving=request.form['driving']
        rid=request.form['rid']

        if address=="":
            address1=""
        else:
            address1=obj.encrypt(address)
        if address2=="":
            address21=""
        else:
            address21=obj.encrypt(address2)

        if pincode=="":
            pincode1=""
        else:
            pincode1=obj.encrypt(pincode)

        if city=="":
            city1=""
        else:
            city1=obj.encrypt(city)
        if state=="":
            state1=""
        else:
            state1=obj.encrypt(state)
        if country=="":
            country1=""
        else:
            country1=obj.encrypt(country)
        if email=="":
            email1=""
        else:
            email1=obj.encrypt(email)
        if mobile=="":
            mobile1=""
        else:
            mobile1=obj.encrypt(mobile)
        if mobile2=="":
            mobile21=""
        else:
            mobile21=obj.encrypt(mobile2)
        if landline=="":
            landline1=""
        else:
            landline1=obj.encrypt(landline)
        if adhar=="":
            adhar1=""
        else:
            adhar1=obj.encrypt(adhar)
        if voter=="":
            voter1=""
        else:
            voter1=obj.encrypt(voter)
        if pancard=="":
            pancard1=""
        else:
            pancard1=obj.encrypt(pancard)
        if driving=="":
            driving1=""
        else:
            driving1=obj.encrypt(driving)

        

        mycursor.execute("update vb_register set address=%s,address2=%s,pincode=%s,city=%s,state=%s,country=%s,email=%s,mobile=%s,mobile2=%s,landline=%s,adhar=%s,voter=%s,pancard=%s,driving=%s,rid=%s where uname=%s",(address1,address21,pincode1,city1,state1,country1,email1,mobile1,mobile21,landline1,adhar1,voter1,pancard1,driving1,rid,uname))
        mydb.commit()
        return redirect(url_for('user_home'))
    

    return render_template('edit.html',data=data,data2=data2,data3=data3,act=act,uname=uname)

@app.route('/edit_account', methods=['GET', 'POST'])
def edit_account():
    msg=""
    act=request.args.get("act")
    sid=request.args.get("sid")
    uname=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    mycursor.execute("SELECT * FROM vb_relative where uname=%s",(uname, ))
    dat3 = mycursor.fetchall()
    data3=[]
    for rs3 in dat3:
        dt3=[]
        dt3.append(rs3[0])
        dt3.append(rs3[1])
        dt3.append(obj.decrypt(rs3[2].encode("utf-8")))
        data3.append(dt3)

    mycursor.execute("SELECT * FROM vb_account where uname=%s && id=%s",(uname,sid ))
    dd = mycursor.fetchone()

    
    data2.append(dd[0])
    data2.append(dd[1])
    data2.append(dd[2])
    if dd[3]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[3].encode("utf-8")))
    if dd[4]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[4].encode("utf-8")))
    if dd[5]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[5].encode("utf-8")))
    if dd[6]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[6].encode("utf-8")))
    if dd[7]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[7].encode("utf-8")))
    if dd[8]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[8].encode("utf-8")))
    
   
    
        
    if request.method=='POST':
        bank=request.form['bank']
        branch=request.form['branch']
        account=request.form['account']
        pinno=request.form['pinno']
        cardno=request.form['cardno']
        acpass=request.form['acpass']
        rid=request.form['rid']

        if bank=="":
            bank1=""
        else:
            bank1=obj.encrypt(bank)

        if branch=="":
            branch1=""
        else:
            branch1=obj.encrypt(branch)

        if account=="":
            account1=""
        else:
            account1=obj.encrypt(account)
        if pinno=="":
            pinno1=""
        else:
            pinno1=obj.encrypt(pinno)
        if cardno=="":
            cardno1=""
        else:
            cardno1=obj.encrypt(cardno)
        if acpass=="":
            acpass1=""
        else:
            acpass1=obj.encrypt(acpass)

        mycursor.execute("update vb_account set bank=%s,branch=%s,account=%s,pinno=%s,cardno=%s,acpass=%s,rid=%s where id=%s",(bank1,branch1,account1,pinno1,cardno1,acpass1,rid,sid))
        mydb.commit()
        return redirect(url_for('account'))
        
        

    return render_template('edit_account.html',data=data,data2=data2,data3=data3,act=act,uname=uname)

@app.route('/edit_audio', methods=['GET', 'POST'])
def edit_audio():
    msg=""
    act=request.args.get("act")
    sid=request.args.get("sid")
    uname=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    mycursor.execute("SELECT * FROM vb_relative where uname=%s",(uname, ))
    dat3 = mycursor.fetchall()
    data3=[]
    for rs3 in dat3:
        dt3=[]
        dt3.append(rs3[0])
        dt3.append(rs3[1])
        dt3.append(obj.decrypt(rs3[2].encode("utf-8")))
        data3.append(dt3)

    mycursor.execute("SELECT * FROM vb_audio where uname=%s && id=%s",(uname,sid ))
    dd = mycursor.fetchone()
    
    data2.append(dd[0])
    data2.append(dd[1])
    data2.append(dd[2])
    if dd[3]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[3].encode("utf-8")))
    if dd[4]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[4].encode("utf-8")))
    if dd[5]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[5].encode("utf-8")))
    if dd[6]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[6].encode("utf-8")))
    if dd[7]=="":
        data2.append("")
    else:
        data2.append(dd[7])
    
        
    if request.method=='POST':
        title=request.form['title']
        details=request.form['details']
        rid=request.form['rid']

        if title=="":
            title1=""
        else:
            title1=obj.encrypt(title)

        if details=="":
            details1=""
        else:
            details1=obj.encrypt(details)

        mycursor.execute("update vb_audio set title=%s,details=%s,rid=%s where id=%s",(title1,details1,rid,sid))
        mydb.commit()
        return redirect(url_for('audio'))

    return render_template('edit_audio.html',data=data,data2=data2,data3=data3,act=act,uname=uname)

@app.route('/edit_doc', methods=['GET', 'POST'])
def edit_doc():
    msg=""
    act=request.args.get("act")
    sid=request.args.get("sid")
    uname=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    mycursor.execute("SELECT * FROM vb_relative where uname=%s",(uname, ))
    dat3 = mycursor.fetchall()
    data3=[]
    for rs3 in dat3:
        dt3=[]
        dt3.append(rs3[0])
        dt3.append(rs3[1])
        dt3.append(obj.decrypt(rs3[2].encode("utf-8")))
        data3.append(dt3)

    mycursor.execute("SELECT * FROM vb_document where uname=%s && id=%s",(uname,sid ))
    dd = mycursor.fetchone()
    
    data2.append(dd[0])
    data2.append(dd[1])
    data2.append(dd[2])
    if dd[3]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[3].encode("utf-8")))
    if dd[4]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[4].encode("utf-8")))
    if dd[5]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[5].encode("utf-8")))
    if dd[6]=="":
        data2.append("")
    else:
        data2.append(dd[6])
    
        
    if request.method=='POST':
        title=request.form['title']
        details=request.form['details']
        rid=request.form['rid']

        if title=="":
            title1=""
        else:
            title1=obj.encrypt(title)

        if details=="":
            details1=""
        else:
            details1=obj.encrypt(details)

        mycursor.execute("update vb_document set title=%s,details=%s,rid=%s where id=%s",(title1,details1,rid,sid))
        mydb.commit()
        return redirect(url_for('document'))

    return render_template('edit_doc.html',data=data,data2=data2,data3=data3,act=act,uname=uname)

@app.route('/edit_email', methods=['GET', 'POST'])
def edit_email():
    msg=""
    act=request.args.get("act")
    sid=request.args.get("sid")
    uname=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    mycursor.execute("SELECT * FROM vb_relative where uname=%s",(uname, ))
    dat3 = mycursor.fetchall()
    data3=[]
    for rs3 in dat3:
        dt3=[]
        dt3.append(rs3[0])
        dt3.append(rs3[1])
        dt3.append(obj.decrypt(rs3[2].encode("utf-8")))
        data3.append(dt3)

    mycursor.execute("SELECT * FROM vb_email where uname=%s && id=%s",(uname,sid ))
    dd = mycursor.fetchone()
    
    
    data2.append(dd[0])
    data2.append(dd[1])
    data2.append(dd[2])
    if dd[3]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[3].encode("utf-8")))
    if dd[4]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[4].encode("utf-8")))
   
        
    if request.method=='POST':
        email=request.form['email']
        pass1=request.form['pass']
        rid=request.form['rid']

        if email=="":
            email1=""
        else:
            email1=obj.encrypt(email)

        if pass1=="":
            pass11=""
        else:
            pass11=obj.encrypt(pass1)

        mycursor.execute("update vb_email set email=%s,pass=%s,rid=%s where id=%s",(email1,pass11,rid,sid))
        mydb.commit()
        return redirect(url_for('ac_email'))
        
        

    return render_template('edit_email.html',data=data,data2=data2,data3=data3,act=act,uname=uname)

@app.route('/edit_relative', methods=['GET', 'POST'])
def edit_relative():
    msg=""
    act=request.args.get("act")
    sid=request.args.get("sid")
    uname=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    mycursor.execute("SELECT * FROM vb_relative where id=%s",(sid, ))
    dd = mycursor.fetchone()
    
  
    data2.append(dd[0])
    data2.append(dd[1])
    if dd[2]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[2].encode("utf-8")))
    if dd[3]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[3].encode("utf-8")))
    if dd[4]=="":
        data2.append("")
    else:
        data2.append(dd[4])
    if dd[5]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[5].encode("utf-8")))
    
        
    if request.method=='POST':
        name=request.form['name']
        relation=request.form['relation']
        mobile=request.form['mobile']
        email=request.form['email']

        if name=="":
            name1=""
        else:
            name1=obj.encrypt(name)
        if relation=="":
            relation1=""
        else:
            relation1=obj.encrypt(relation)
        if mobile=="":
            mobile1=""
        else:
            mobile1=mobile
        if email=="":
            email1=""
        else:
            email1=obj.encrypt(email)

        mycursor.execute("update vb_relative set name=%s,relation=%s,mobile=%s,email=%s where id=%s",(name1,relation1,mobile1,email1,sid))
        mydb.commit()
        return redirect(url_for('relative'))
        
        

    return render_template('edit_relative.html',data=data,data2=data2,act=act,uname=uname)

@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    msg=""
    act=request.args.get("act")
    sid=request.args.get("sid")
    uname=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    data = mycursor.fetchone()
    dat=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    mycursor.execute("SELECT * FROM vb_user where uname=%s && id=%s",(uname,sid ))
    dd = mycursor.fetchone()
    
    data2.append(dd[0])
    data2.append(dd[1])
    if dd[2]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[2].encode("utf-8")))
    if dd[3]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[3].encode("utf-8")))
    if dd[4]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[4].encode("utf-8")))
    if dd[5]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[5].encode("utf-8")))
    if dd[6]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[6].encode("utf-8")))
    if dd[7]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[7].encode("utf-8")))
   

        
    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']

        if name=="":
            name1=""
        else:
            name1=obj.encrypt(name)
        if mobile=="":
            mobile1=""
        else:
            mobile1=obj.encrypt(mobile)
        if email=="":
            email1=""
        else:
            email1=obj.encrypt(email1)
        

        mycursor.execute("update vb_user set name=%s,mobile=%s,email=%s where id=%s",(name1,mobile1,email1,sid))
        mydb.commit()
        return redirect(url_for('add_user'))
        
        

    return render_template('edit_user.html',data=data,data2=data2,act=act,uname=uname)

@app.route('/education', methods=['GET', 'POST'])
def education():
    msg=""
    act=""
    uname=""
    data2=[]
    if 'username' in session:
        uname = session['username']
    
    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))
    

    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dd = mycursor.fetchone()

    if dd[19]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[19].encode("utf-8")))
    if dd[20]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[20].encode("utf-8")))
    if dd[21]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[21].encode("utf-8")))
    if dd[22]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[22].encode("utf-8")))
    if dd[23]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[23].encode("utf-8")))
    if dd[24]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[24].encode("utf-8")))
    if dd[25]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[25].encode("utf-8")))
    if dd[26]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[26].encode("utf-8")))
    if dd[27]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[27].encode("utf-8")))
    if dd[28]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[28].encode("utf-8")))
    if dd[29]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[29].encode("utf-8")))
    if dd[30]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[30].encode("utf-8")))
    if dd[31]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[31].encode("utf-8")))
    if dd[32]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[32].encode("utf-8")))

        


    if request.method=='POST':
        sslc_school=request.form['sslc_school']
        sslc_mark=request.form['sslc_mark']
        sslc_year=request.form['sslc_year']
        sslc_per=request.form['sslc_per']
        hsc_school=request.form['hsc_school']
        hsc_mark=request.form['hsc_mark']
        hsc_year=request.form['hsc_year']
        hsc_per=request.form['hsc_per']
        ug_college=request.form['ug_college']
        ug_per=request.form['ug_per']
        ug_year=request.form['ug_year']
        pg_college=request.form['pg_college']
        pg_per=request.form['pg_per']
        pg_year=request.form['pg_year']

        if sslc_school=="":
            sslc_school1=""
        else:
            sslc_school1=obj.encrypt(sslc_school)   
        if sslc_mark=="":
            sslc_mark1=""
        else:
            sslc_mark1=obj.encrypt(sslc_mark)
        if sslc_year=="":
            sslc_year1=""
        else:
            sslc_year1=obj.encrypt(sslc_year)
        if sslc_per=="":
            sslc_per1=""
        else:
            sslc_per1=obj.encrypt(sslc_per)
        if hsc_school=="":
            hsc_school1=""
        else:
            hsc_school1=obj.encrypt(hsc_school)
        if hsc_mark=="":
            hsc_mark1=""
        else:
            hsc_mark1=obj.encrypt(hsc_mark)
        if hsc_year=="":
            hsc_year1=""
        else:
            hsc_year1=obj.encrypt(hsc_year)
        if hsc_per=="":
            hsc_per1=""
        else:
            hsc_per1=obj.encrypt(hsc_per)
        if ug_college=="":
            ug_college1=""
        else:
            ug_college1=obj.encrypt(ug_college)
        if ug_per=="":
            ug_per1=""
        else:
            ug_per1=obj.encrypt(ug_per)
        if ug_year=="":
            ug_year1=""
        else:
            ug_year1=obj.encrypt(ug_year)
        if pg_college=="":
            pg_college1=""
        else:
            pg_college1=obj.encrypt(pg_college)
        if pg_per=="":
            pg_per1=""
        else:
            pg_per1=obj.encrypt(pg_per)
        if pg_year=="":
            pg_year1=""
        else:
            pg_year1=obj.encrypt(pg_year)

        mycursor.execute("update vb_register set sslc_school=%s,sslc_mark=%s,sslc_year=%s,sslc_per=%s,hsc_school=%s,hsc_mark=%s,hsc_year=%s,hsc_per=%s,ug_college=%s,ug_per=%s,ug_year=%s,pg_college=%s,pg_per=%s,pg_year=%s where uname=%s",(sslc_school1,sslc_mark1,sslc_year1,sslc_per1,hsc_school1,hsc_mark1,hsc_year1,hsc_per1,ug_college1,ug_per1,ug_year1,pg_college1,pg_per1,pg_year1,uname))
        mydb.commit()
        return redirect(url_for('user_home'))
    

    return render_template('education.html',data=data,data2=data2,act=act,uname=uname)

@app.route('/occupation', methods=['GET', 'POST'])
def occupation():
    msg=""
    act=request.args.get("act")
    uname=""
    st=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    if request.method=='POST':
        company=request.form['company']
        position=request.form['position']
        salary=request.form['salary']
        duration=request.form['duration']
        experience=request.form['experience']

        
        if company=="":
            company1=""
        else:
            company1=obj.encrypt(company)
        if position=="":
            position1=""
        else:
            position1=obj.encrypt(position)
        if salary=="":
            salary1=""
        else:
            salary1=obj.encrypt(salary)
        if duration=="":
            duration1=""
        else:
            duration1=obj.encrypt(duration)
        if experience=="":
            experience1=""
        else:
            experience1=obj.encrypt(experience)

        mycursor.execute("SELECT max(id)+1 FROM vb_occupation")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        rdate1=obj.encrypt(rdate)
        
        sql = "INSERT INTO vb_occupation(id,uname,company,position,experience,salary,duration,rdate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,company1,position1,experience1,salary1,duration1,rdate1)
        mycursor.execute(sql, val)
        mydb.commit()
 
        print(mycursor.rowcount, "Registered Success")
        msg="success"

    mycursor.execute("SELECT count(*) FROM vb_occupation where uname=%s",(uname, ))
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        st="1"
        mycursor.execute("SELECT * FROM vb_occupation where uname=%s",(uname, ))
        dd = mycursor.fetchall()
        for rr in dd:
            dt=[]
            dt.append(rr[0])
            dt.append(rr[1])
            dt.append(rr[2])
            if rr[3]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[3].encode("utf-8")))
            if rr[4]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[4].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[5].encode("utf-8")))
            if rr[6]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[6].encode("utf-8")))
            if rr[7]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[7].encode("utf-8")))
            
            

            na=""
            if rr[1]==0:
                na=""
            else:
                mycursor.execute("SELECT * FROM vb_relative where id=%s",(rr[1], ))
                r2 = mycursor.fetchone()
                na=obj.decrypt(r2[2].encode("utf-8"))

            dt.append(na)
            data2.append(dt)
            
        


    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from vb_occupation where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('occupation'))

    return render_template('occupation.html',msg=msg,data=data,data2=data2,act=act,st=st,uname=uname)



@app.route('/sendto', methods=['GET', 'POST'])
def sendto():
    msg=""
    act=request.args.get("act")
    sid=request.args.get("sid")
    uname=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    mycursor.execute("SELECT * FROM vb_relative where uname=%s",(uname, ))
    dat3 = mycursor.fetchall()
    data3=[]
    for rs3 in dat3:
        dt3=[]
        dt3.append(rs3[0])
        dt3.append(rs3[1])
        dt3.append(obj.decrypt(rs3[2].encode("utf-8")))
        data3.append(dt3)

    mycursor.execute("SELECT * FROM vb_occupation where uname=%s && id=%s",(uname,sid ))
    dd = mycursor.fetchone()
    
    data2.append(dd[0])
    data2.append(dd[1])
    data2.append(dd[2])
    if dd[3]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[3].encode("utf-8")))
    if dd[4]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[4].encode("utf-8")))
    if dd[5]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[5].encode("utf-8")))
    if dd[6]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[6].encode("utf-8")))
    if dd[7]=="":
        data2.append("")
    else:
        data2.append(obj.decrypt(dd[7].encode("utf-8")))
    
        
    if request.method=='POST':
        company=request.form['company']
        position=request.form['position']
        salary=request.form['salary']
        duration=request.form['duration']
        experience=request.form['experience']
        rid=request.form['rid']

        if company=="":
            company1=""
        else:
            company1=obj.encrypt(company)
        if position=="":
            position1=""
        else:
            position1=obj.encrypt(position)
        if salary=="":
            salary1=""
        else:
            salary1=obj.encrypt(salary)
        if duration=="":
            duration1=""
        else:
            duration1=obj.encrypt(duration)
        if experience=="":
            experience1=""
        else:
            experience1=obj.encrypt(experience)

        mycursor.execute("update vb_occupation set company=%s,position=%s,salary=%s,duration=%s,experience=%s,rid=%s where id=%s",(company1,position1,salary1,duration1,experience1,rid,sid))
        mydb.commit()
        return redirect(url_for('occupation'))
        
        

    return render_template('sendto.html',data=data,data2=data2,data3=data3,act=act,uname=uname)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']
    
    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    if request.method=='POST':
        file = request.files['file']
        fname = file.filename
        filename = secure_filename(fname)
        photo="U"+str(dat[0])+filename
        photo1=obj.encrypt(photo)
        file.save(os.path.join("static/photo", photo))
        mycursor.execute("update vb_register set photo=%s where uname=%s",(photo1,uname))
        mydb.commit()
        
        return redirect(url_for('user_home'))

    return render_template('upload.html',data=data,act=act,uname=uname)

@app.route('/setting', methods=['GET', 'POST'])
def setting():
    msg=""
    act=request.args.get("act")
    uname=""
    st=""
    act_st=""
    data2=[]
    if 'username' in session:
        uname = session['username']

    ky=uname
    obj=AESCipher(ky)
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(uname, ))
    dat = mycursor.fetchone()
    data=[]
    data.append(dat[0])
    data.append(obj.decrypt(dat[1].encode("utf-8")))
    data.append(obj.decrypt(dat[2].encode("utf-8")))

    active=dat[43]
    if active==1:
        act_st="1"
    else:
        act_st="2"
    
    if dat[33]=="":
        data.append("")
    else:
        data.append(obj.decrypt(dat[33].encode("utf-8")))

    if act=="yes":
        mycursor.execute("update vb_register set alert_st=0 where uname=%s",(uname,))
        mydb.commit()
        return redirect(url_for('setting'))
    if act=="no":
        mycursor.execute("update vb_register set alert_st=1 where uname=%s",(uname,))
        mydb.commit()
        return redirect(url_for('setting'))

    if act=="died":
        msg="sent2"
        

        mycursor.execute("update vb_register set active_st=1 where uname=%s",(uname,))
        mydb.commit()

        mycursor.execute("SELECT * FROM vb_relative where uname=%s",(uname, ))
        dat2 = mycursor.fetchall()
        for dd2 in dat2:
            rid=dd2[0]
            rname=obj.decrypt(dd2[2].encode("utf-8"))
            mob1=dd2[4]
            email1=obj.decrypt(dd2[5].encode("utf-8"))
            p1=obj.decrypt(dd2[6].encode("utf-8"))
            kk1=randint(100,500)
            kk2=randint(500,950)
            kk=str(kk1)+str(kk2)
            mycursor.execute("update vb_relative set secret_key=%s where id=%s",(kk,rid))
            mydb.commit()

            dt=[]
            mess1="Dear "+rname+", Received information from "+uname+", Username:"+mob1+", Password:"+p1+", Key: "+kk+", Link: http://localhost:5000/login";
            print(mess1)
            print(email1)
            dt.append(mess1)
            dt.append(email1)
            data2.append(dt)

    if act=="sendmail":
        msg="sent"


        mycursor.execute("SELECT * FROM vb_relative where uname=%s",(uname, ))
        dat2 = mycursor.fetchall()
        for dd2 in dat2:
            rid=dd2[0]
            rname=obj.decrypt(dd2[2].encode("utf-8"))
            mob1=dd2[4]
            email1=obj.decrypt(dd2[5].encode("utf-8"))
            p1=obj.decrypt(dd2[6].encode("utf-8"))
            kk1=randint(100,500)
            kk2=randint(500,950)
            kk=str(kk1)+str(kk2)
            mycursor.execute("update vb_relative set secret_key=%s where id=%s",(kk,rid))
            mydb.commit()

            dt=[]
            mess1="Dear "+rname+", Received information from "+uname+", Username:"+mob1+", Password:"+p1+", Key: "+kk+", Link: http://localhost:5000/login";
            print(mess1)
            print(email1)
            dt.append(mess1)
            dt.append(email1)
            data2.append(dt)

    return render_template('setting.html',msg=msg,data=data,act=act,st=st,uname=uname,data2=data2,act_st=act_st)

@app.route('/home', methods=['GET', 'POST'])
def home():
    msg=""
    act=""
    uname=""
    rid=""
    rname=""
    data=[]
    data2=[]
    data3=[]
    data4=[]
    data5=[]
    data6=[]


    st1=""
    st2=""
    st3=""
    st4=""
    st5=""
    st6=""
    
    if 'username' in session:
        uname = session['username']
        rid = session['rid']
    print(uname)
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM vb_relative where id=%s",(rid,))
    rr = mycursor.fetchone()
    un=rr[1]
    ky=un
    obj=AESCipher(ky)
    rname=obj.decrypt(rr[2].encode("utf-8"))

    mycursor.execute("SELECT count(*) FROM vb_register where uname=%s && rid=%s",(un,rid ))
    cnt1 = mycursor.fetchone()[0]
    if cnt1>0:
        st1="1"
        mycursor.execute("SELECT * FROM vb_register where uname=%s && rid=%s",(un,rid ))
        data = mycursor.fetchone()

    #######################################
    mycursor.execute("SELECT count(*) FROM vb_occupation where uname=%s && rid=%s",(un,rid ))
    cnt2 = mycursor.fetchone()[0]
    if cnt2>0:
        st2="1"
        mycursor.execute("SELECT * FROM vb_occupation where uname=%s && rid=%s",(un,rid ))
        data2 = mycursor.fetchall()
        
    ##########################
    mycursor.execute("SELECT count(*) FROM vb_account where uname=%s && rid=%s",(un,rid ))
    cnt3 = mycursor.fetchone()[0]
    if cnt3>0:
        st3="1"
        mycursor.execute("SELECT * FROM vb_account where uname=%s && rid=%s",(un,rid ))
        data3 = mycursor.fetchall()
        
    #####################################
    mycursor.execute("SELECT count(*) FROM vb_email where uname=%s && rid=%s",(un,rid ))
    cnt4 = mycursor.fetchone()[0]
    if cnt4>0:
        st4="1"
        mycursor.execute("SELECT * FROM vb_email where uname=%s && rid=%s",(un,rid ))
        data4 = mycursor.fetchall()
        
    #################################
    mycursor.execute("SELECT count(*) FROM vb_document where uname=%s && rid=%s",(un,rid ))
    cnt5 = mycursor.fetchone()[0]
    if cnt5>0:
        st5="1"
        mycursor.execute("SELECT * FROM vb_document where uname=%s && rid=%s",(un,rid ))
        data5 = mycursor.fetchall()
        
    #################################
    mycursor.execute("SELECT count(*) FROM vb_audio where uname=%s && rid=%s",(un,rid ))
    cnt6 = mycursor.fetchone()[0]
    if cnt6>0:
        st6="1"
        mycursor.execute("SELECT * FROM vb_audio where uname=%s && rid=%s",(un,rid ))
        data6 = mycursor.fetchall()
        
    #########################################
            


    return render_template('home.html',data=data,act=act,rname=rname,uname=uname,rid=rid,st1=st1,st2=st2,st3=st3,st4=st4,st5=st5,st6=st6,data2=data2,data3=data3,data4=data4,data5=data5,data6=data6)

@app.route('/home2', methods=['GET', 'POST'])
def home2():
    msg=""
    act=request.args.get("act")
    uname=""
    rid=""
    rname=""
    data=[]
    data2=[]
    data3=[]
    data4=[]
    data5=[]
    data6=[]


    st1=""
    st2=""
    st3=""
    st4=""
    st5=""
    st6=""
    
    if 'username' in session:
        uname = session['username']
        rid = session['rid']
    print(uname)
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM vb_relative where id=%s",(rid,))
    rr = mycursor.fetchone()
    un=rr[1]
    ky=un
    obj=AESCipher(ky)
    rname=obj.decrypt(rr[2].encode("utf-8"))

    mycursor.execute("SELECT count(*) FROM vb_register where uname=%s && rid=%s",(un,rid ))
    cnt1 = mycursor.fetchone()[0]
    if cnt1>0:
        st1="1"
        mycursor.execute("SELECT * FROM vb_register where uname=%s && rid=%s",(un,rid ))
        dat = mycursor.fetchone()

        
       
        #fname=obj.decrypt(dat[1].encode("utf-8"))
        data.append(dat[0])
        data.append(obj.decrypt(dat[1].encode("utf-8")))
        data.append(obj.decrypt(dat[2].encode("utf-8")))
        data.append(obj.decrypt(dat[3].encode("utf-8")))
        data.append(obj.decrypt(dat[4].encode("utf-8")))
        data.append(obj.decrypt(dat[5].encode("utf-8")))
        data.append(obj.decrypt(dat[6].encode("utf-8")))
        data.append(obj.decrypt(dat[7].encode("utf-8")))
        data.append(obj.decrypt(dat[8].encode("utf-8")))
        data.append(obj.decrypt(dat[9].encode("utf-8")))
        data.append(obj.decrypt(dat[10].encode("utf-8")))
        data.append(obj.decrypt(dat[11].encode("utf-8")))
        data.append(obj.decrypt(dat[12].encode("utf-8")))
        data.append(obj.decrypt(dat[13].encode("utf-8")))
        data.append(obj.decrypt(dat[14].encode("utf-8")))
        data.append(obj.decrypt(dat[15].encode("utf-8")))
        data.append(obj.decrypt(dat[16].encode("utf-8")))
        data.append(obj.decrypt(dat[17].encode("utf-8")))
        data.append(obj.decrypt(dat[18].encode("utf-8")))

        if dat[19]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[19].encode("utf-8")))

        if dat[20]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[20].encode("utf-8")))
            
        if dat[21]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[21].encode("utf-8")))

        if dat[22]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[22].encode("utf-8")))

        if dat[23]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[23].encode("utf-8")))

        if dat[24]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[24].encode("utf-8")))

        if dat[25]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[25].encode("utf-8")))

        if dat[26]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[26].encode("utf-8")))

        if dat[27]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[27].encode("utf-8")))

        if dat[28]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[28].encode("utf-8")))

        if dat[29]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[29].encode("utf-8")))

        if dat[30]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[30].encode("utf-8")))

        if dat[31]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[31].encode("utf-8")))

        if dat[32]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[32].encode("utf-8")))

        if dat[33]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[33].encode("utf-8")))

        data.append(dat[34])
        data.append(obj.decrypt(dat[35].encode("utf-8")))
        if dat[36]=="":
            data.append("")
        else:
            data.append(obj.decrypt(dat[36].encode("utf-8")))
        data.append(dat[37])
        data.append(dat[38])
        data.append(dat[39])
        data.append(dat[40])
        data.append(obj.decrypt(dat[41].encode("utf-8")))
        data.append(dat[42])
        data.append(dat[43])
    #######################################
    mycursor.execute("SELECT count(*) FROM vb_occupation where uname=%s && rid=%s",(un,rid ))
    cnt2 = mycursor.fetchone()[0]
    if cnt2>0:
        st2="1"
        mycursor.execute("SELECT * FROM vb_occupation where uname=%s && rid=%s",(un,rid ))
        dd = mycursor.fetchall()
        for rr in dd:
            dt=[]
            dt.append(rr[0])
            dt.append(rr[1])
            dt.append(rr[2])
            if rr[3]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[3].encode("utf-8")))
            if rr[4]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[4].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[5].encode("utf-8")))
            if rr[6]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[6].encode("utf-8")))
            if rr[7]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[7].encode("utf-8")))
            data2.append(dt)
    ##########################
    mycursor.execute("SELECT count(*) FROM vb_account where uname=%s && rid=%s",(un,rid ))
    cnt3 = mycursor.fetchone()[0]
    if cnt3>0:
        st3="1"
        mycursor.execute("SELECT * FROM vb_account where uname=%s && rid=%s",(un,rid ))
        dd = mycursor.fetchall()
        for rr in dd:
            dt=[]
            dt.append(rr[0])
            dt.append(rr[1])
            dt.append(rr[2])
            
            if rr[3]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[3].encode("utf-8")))
            if rr[4]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[4].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[5].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[6].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[7].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[8].encode("utf-8")))

            data3.append(dt)
    #####################################
    mycursor.execute("SELECT count(*) FROM vb_email where uname=%s && rid=%s",(un,rid ))
    cnt4 = mycursor.fetchone()[0]
    if cnt4>0:
        st4="1"
        mycursor.execute("SELECT * FROM vb_email where uname=%s && rid=%s",(un,rid ))
        dd = mycursor.fetchall()
        for rr in dd:
            dt=[]
            dt.append(rr[0])
            dt.append(rr[1])
            dt.append(rr[2])
            
            if rr[3]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[3].encode("utf-8")))
            if rr[4]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[4].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[5].encode("utf-8")))

            data4.append(dt)
    #################################
    mycursor.execute("SELECT count(*) FROM vb_document where uname=%s && rid=%s",(un,rid ))
    cnt5 = mycursor.fetchone()[0]
    if cnt5>0:
        st5="1"
        mycursor.execute("SELECT * FROM vb_document where uname=%s && rid=%s",(un,rid ))
        dd = mycursor.fetchall()
        for rr in dd:
            dt=[]
            dt.append(rr[0])
            dt.append(rr[1])
            dt.append(rr[2])
            if rr[3]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[3].encode("utf-8")))
            if rr[4]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[4].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[5].encode("utf-8")))

            data5.append(dt)
    #################################
    mycursor.execute("SELECT count(*) FROM vb_audio where uname=%s && rid=%s",(un,rid ))
    cnt6 = mycursor.fetchone()[0]
    if cnt6>0:
        st6="1"
        mycursor.execute("SELECT * FROM vb_audio where uname=%s && rid=%s",(un,rid ))
        dd = mycursor.fetchall()
        for rr in dd:
            dt=[]
            dt.append(rr[0])
            dt.append(rr[1])
            dt.append(rr[2])
            if rr[3]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[3].encode("utf-8")))
            if rr[4]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[4].encode("utf-8")))
            if rr[5]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[5].encode("utf-8")))
            if rr[6]=="":
                dt.append("")
            else:
                dt.append(obj.decrypt(rr[6].encode("utf-8")))

            data6.append(dt)
    #########################################
    if act=="down":
        fid=request.args.get("fid")
        mycursor.execute("SELECT * FROM vb_document where id=%s",(fid, ))
        r3 = mycursor.fetchone()
        fname=obj.decrypt(r3[5].encode("utf-8"))
        ##
        password_provided = ky # This is input in the form of a string
        password = password_provided.encode() # Convert to type bytes
        salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        input_file = 'static/document/'+fname
        output_file = 'static/down/'+fname
        with open(input_file, 'rb') as f:
            dataa = f.read()

        fernet = Fernet(key)
        encrypted = fernet.decrypt(dataa)

        with open(output_file, 'wb') as f:
            f.write(encrypted)
        ##
        return redirect(url_for('down',fname=fname))
    ###########################################
    if act=="down2":
        fid=request.args.get("fid")
        mycursor.execute("SELECT * FROM vb_audio where id=%s",(fid, ))
        r3 = mycursor.fetchone()
        fname=obj.decrypt(r3[6].encode("utf-8"))
        ##
        password_provided = ky # This is input in the form of a string
        password = password_provided.encode() # Convert to type bytes
        salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        input_file = 'static/audio/'+fname
        output_file = 'static/down/'+fname
        with open(input_file, 'rb') as f:
            dataa = f.read()

        fernet = Fernet(key)
        encrypted = fernet.decrypt(dataa)

        with open(output_file, 'wb') as f:
            f.write(encrypted)
        ##
        return redirect(url_for('down',fname=fname))

    return render_template('home2.html',data=data,act=act,rname=rname,uname=uname,rid=rid,st1=st1,st2=st2,st3=st3,st4=st4,st5=st5,st6=st6,data2=data2,data3=data3,data4=data4,data5=data5,data6=data6)



@app.route('/home_dec', methods=['GET', 'POST'])
def home_dec():
    msg=""
    act=""
    uname=""
    rid=""
    rname=""
    data=[]
    if 'username' in session:
        uname = session['username']
        rid = session['rid']
    print(uname)
    
        
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM vb_relative where id=%s",(rid,))
    rr = mycursor.fetchone()
    un=rr[1]
    ky=un
    obj=AESCipher(ky)
    rname=obj.decrypt(rr[2].encode("utf-8"))
    skey=rr[8]
    mycursor.execute("SELECT * FROM vb_register where uname=%s",(un, ))
    dat = mycursor.fetchone()

    

    if request.method=='POST':
        secret=request.form['secret']
        if skey==secret:
            return redirect(url_for('home2'))
        else:
            msg="Secret Key Wrong!"
            

    return render_template('home_dec.html',msg=msg,act=act,rname=rname,uname=uname,rid=rid)

@app.route('/down', methods=['GET', 'POST'])
def down():
    fn = request.args.get('fname')
    path="static/down/"+fn
    return send_file(path, as_attachment=True)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
