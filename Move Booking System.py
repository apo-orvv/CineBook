def dbcon():
    # Initial Script to create database schema
    import mysql.connector as myc

    try:
        con = myc.connect(host='localhost',user='root',passwd='apoorv')
        mycursor = con.cursor()
        mycursor.execute('DROP DATABASE IF EXISTS cinemaproj')
        mycursor.execute('CREATE DATABASE cinemaproj')
        mycursor.execute('USE cinemaproj')
        mycursor.execute('DROP TABLE IF EXISTS hall_det')
        sql = '''CREATE TABLE hall_det(
                    hallno INT(4) PRIMARY KEY,
                    hallname VARCHAR(20) NOT NULL,
                    frontseats INT(3) NOT NULL,
                    midseats INT(3) NOT NULL,
                    backseats INT(3) NOT NULL)'''
        mycursor.execute(sql)
        mycursor.execute('DROP TABLE IF EXISTS booking_det')
        sql = '''CREATE TABLE booking_det(
                    tickectno INT(5) PRIMARY KEY,
                    hallno INT(5) NOT NULL,
                    customer VARCHAR(15) NOT NULL,
                    no_of_seats INT(2) NOT NULL,
                    cost_of_seat INT(4) NOT NULL,
                    seattype CHAR(1) NOT NULL,
                    discount INT(3) NULL,
                    CONSTRAINT FOREIGN KEY(hallno) 
                    REFERENCES hall_det(hallno))'''
        mycursor.execute(sql)

        #Inserting Rows in to the Cinema hall table
        sql = """INSERT INTO hall_det(hallno, hallname, frontseats, midseats,backseats)
        VALUES(%s, %s, %s, %s, %s)"""
        rows = [(1001,'PVR-YPR',50,50,50),(1002,'INOX-MANTRI',50,50,50),\
        (1003,'PVR-GOP',50,50,50),(1004,'PHOENIX',60,50,50)]
        mycursor.executemany(sql, rows)
        con.commit()
    except myc.Error as err:
        print(err)
        print("SQLSTATE", err.sqlstate)
    finally:
        print('Database Schema Created')
        


#Function to retuen the number of seats available in a hall
def getseats(hno):
    try:
        import mysql.connector as myc
        con = myc.connect(host='localhost',user='root',passwd='apoorv', database='cinemaproj')
        mycursor=con.cursor()
        sql = "SELECT frontseats, midseats, backseats FROM hall_det WHERE hallno='%d'" % (hno)
        mycursor.execute(sql)
        rec = mycursor.fetchone()
        con.close()
    except myc.Error as err:
        print(err)
    finally:
        return rec

#Function to get all the hall numbers
def hallnums():
    try:
        import mysql.connector as myc
        con = myc.connect(host='localhost',user='root',passwd='apoorv', database='cinemaproj')
        mycursor=con.cursor()
        sql = "SELECT hallno FROM hall_det ORDER BY hallno"
        mycursor.execute(sql)
        rec = mycursor.fetchall()
        hlst =[]
        for x in rec:
            hlst.append(x[0])
    except myc.Error as err:
        print(err)
    finally:
        return hlst

#Function to get all ticket numbers
def getticketdet():
    try:
        import mysql.connector as myc
        con = myc.connect(host='localhost',user='root',passwd='apoorv', database='cinemaproj')
        mycursor=con.cursor()
        sql = "SELECT tickectno FROM booking_det"
        mycursor.execute(sql)
        rec = mycursor.fetchall()
        tlst =[]
        for x in rec:
            tlst.append(x[0])
    except myc.Error as err:
        print(err)
    finally:
        
        return tlst

#Function to update the seats based on bookings
def updateseats(hno,stype,amt):
    try:
        import mysql.connector as myc
        con = myc.connect(host='localhost',user='root',passwd='apoorv', database='cinemaproj')
        mycursor=con.cursor()
        if stype=='A':
            sql = "UPDATE hall_det SET frontseats=frontseats-%d WHERE hallno=%d;" % (amt,hno)
        if stype=='B':
            sql = "UPDATE hall_det SET midseats=midseats-%d WHERE hallno=%d;" % (amt,hno)
        if stype=='C':
            sql = "UPDATE hall_det SET backseats=backseats-%d WHERE hallno=%d;" % (amt,hno)
        mycursor.execute(sql)
        con.commit()    
    except myc.Error as err:
        print(err)
    finally:
        print('Seats updated')
        
    
#Function to book the seats and also call update seats function     
def booking(hno, cname,noseat, cost,stype, disc=0):
    import mysql.connector as myc
    s1,s2,s3=getseats(hno)
    if (stype=='A' and noseat>s1) or (stype=='B' and noseat>s2) or (stype=='C' and noseat>s3):
        return 'No seats available'
    else:
        try:
            import random as rd
            rec=getticketdet()
            ticno=rd.randint(100,999)
            while ticno in rec:
                ticno=rd.randint(100,999)
            con = myc.connect(host='localhost',user='root',passwd='apoorv', database='cinemaproj')
            mycursor=con.cursor()
            sql="INSERT INTO booking_det(tickectno,hallno,customer,no_of_seats,cost_of_seat,seattype, discount) \
            VALUES(%s,%s,%s,%s,%s,%s,%s);" 
            rows=[(ticno,hno, cname,noseat, cost,stype, disc)]
            mycursor.executemany(sql,rows)
            con.commit()
            #update the seats after booking
            updateseats(hno,stype,noseat)                
        except myc.Error as err:
            print(err)
        finally:
            print('Record Inserted')
            print('Your Ticket Number is '+str(ticno))
                
#booking(1001,'Ashok',4,500,'A',0)  

#Function to display booking details for a given hall
def showhallbooking(hno):
    try:
        import mysql.connector as myc
        con = myc.connect(host='localhost',user='root',passwd='apoorv', database='cinemaproj')
        mycursor=con.cursor()
        sql = "SELECT b.tickectno, b.hallno, h.hallname, b.seattype, b.no_of_seats, b.cost_of_seat, b.discount\
        FROM booking_det b, hall_det h WHERE b.hallno=h.hallno and b.hallno=%d;" % (hno)
        mycursor.execute(sql)
        rec = mycursor.fetchall()
    except myc.Error as err:
        print(err)
        print("SQLSTATE", err.sqlstate)
    finally:
        return rec
#print(showhallbooking(1001))

#Function to print the hall status
def hallstat():
    try:
        import mysql.connector as myc
        con = myc.connect(host='localhost',user='root',passwd='apoorv', database='cinemaproj')
        mycursor=con.cursor()
        sql = "SELECT hallno, hallname,frontseats, midseats, backseats FROM hall_det" 
        mycursor.execute(sql)
        rec = mycursor.fetchall()
    except myc.Error as err:
        print(err)
        print("SQLSTATE", err.sqlstate)
    finally:
        
        return rec
#print(hallstat())  
#function to display all bookings
def allbookings():
    try:
        import mysql.connector as myc
        con = myc.connect(host='localhost',user='root',passwd='apoorv', database='cinemaproj')
        mycursor=con.cursor()
        sql = "SELECT b.tickectno, h.hallno, h.hallname, b.seattype, b.no_of_seats, b.cost_of_seat, b.discount,\
        h.frontseats, h.midseats, h.backseats FROM booking_det b, hall_det h WHERE b.hallno=h.hallno"
        mycursor.execute(sql)
        rec = mycursor.fetchall()
    except myc.Error as err:
        print(err)
        print("SQLSTATE", err.sqlstate)
    finally:
        
        return rec
#print(allbookings())

def addhall(hname, fs,ms,bs):
    try:
        import random as rd
        rec=hallnums()
        hallno=rd.randint(1000,9990)
        while hallno in rec:
            hallno=rd.randint(1000,9999)
        import mysql.connector as myc
        con = myc.connect(host='localhost',user='root',passwd='apoorv', database='cinemaproj')
        mycursor=con.cursor()
        sql="INSERT INTO hall_det(hallno,hallname, frontseats, midseats, backseats) VALUES(%s,%s,%s,%s,%s)" 
        rows=[(hallno,hname,fs,ms,bs)]
        mycursor.executemany(sql,rows)
        con.commit()
    except myc.Error as err:
        print(err)
        print("SQLSTATE", err.sqlstate)
    finally:
        print('Hall added')
        print('Hall No. of your added Hall is '+str(hallno))
        
#addhall('VAISHNAVI-SAPPHIRE', 100,100,100) 

def printticket(tno):
    
    try:
        import mysql.connector as myc
        con = myc.connect(host='localhost',user='root',passwd='apoorv', database='cinemaproj')
        mycursor=con.cursor()
        sql = "SELECT b.tickectno, b.hallno, h.hallname, b.customer,b.seattype, b.no_of_seats, b.cost_of_seat, b.discount\
        FROM booking_det b, hall_det h WHERE b.hallno=h.hallno and b.tickectno='%d'" % (tno)
        mycursor.execute(sql)
        rec = mycursor.fetchall()
    except myc.Error as err:
        print(err)
        print("SQLSTATE", err.sqlstate)
    finally:
        
        return rec
#print(printticket(101))  

#Function to enforce integer input. Use this while accepting integers
def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print("Not an integer! Try again.")
       continue
    else:
       return userInput 
       break  
    




import os, sys

while True:

    print('||==============Book My Show===================||')
    print('||      You can perform the following tasks    ||')
    print('|| Type 0 to reset Application                 ||')
    print('|| Type 1 to add a hall in your portal         ||')
    print('|| Type 2 to view all the halls in your portal ||')
    print('|| Type 3 to see the booking status of a hall  ||')
    print('|| Type 4 to book a ticket in a hall           ||')
    print('|| Type 5 to see booking of all the halls      ||')
    print('|| Type 6 to generate ticket for booking       ||')
    print('|| Type 7 to quit                              ||')
    print('||=============================================||')
    choice=int(input('Enter your choice:'))
    if choice==0:
        dbcon()
    if choice == 1:
        hname=input('Enter your hall name:')
        fs = int(input('Enter the maximum front seats:'))
        ms = int(input('Enter the maximum middle seats:'))
        bs = int(input('Enter the maximum back seats:'))
        addhall(hname,fs,ms,bs)
    if choice==2:
        import pandas as pd
        rec=hallstat()
        df = pd.DataFrame(rec)
        df.columns= ['Hall No', 'Hall Name', 'A-Type', 'B-Type', 'C-Type']
        df.index=[i for i in range(1,len(rec)+1)]
        print(df)
    if choice==3:
        import pandas as pd
        print('You can get details of the following hall Numbers')
        print(hallnums())
        hno=int(input('Enter a valid hallno:'))
        if hno in hallnums():
            rec = showhallbooking(hno)
            if rec!=[]:
                df=pd.DataFrame(rec)
                df.columns = ['Ticket No','Hall No','Hall Name','Seat Type','No of Seate','Rate','Discount']
                df.index=[i for i in range(1,len(rec)+1)]
                print(df)
            else:
                print('No tickets booked in this hall!')
        else:
            print('Invalid Hall Number')
    if choice==4:
        import pandas as pd
        print('You have the following hall numbers')
        print(hallnums())
        hno=int(input('Enter a valid hallno:'))
        cname=input('Enter Customer name:')
        stype=input('Enter Seat Type(A,B,C):')
        noseat=int(input('Enter number of seats:'))
        cost = int(input('Enter cost of each seat:'))
        dis=0
        if noseat*cost>=2000:
            dis=100
        booking(hno,cname,noseat,cost,stype,dis)
    
    if choice==5:
        import pandas as pd
        rec = allbookings()
        df=pd.DataFrame(rec)
        df.columns=['Ticket No','Hall No','Hall Name','Seat Type','No of Seats',\
        'Cost per seat','Discount','A-Type','B-Type','C-Type']
        df.index=[i for i in range(1,len(rec)+1)]
        print(df)
    if choice==6:
        tno = int(input('Enter the ticket number:'))
        rec = getticketdet()
        if tno in rec:
            rec = printticket(tno)
            print("---------Ticket Details-----------")
            print("Ticket Number is   :%d" % (rec[0][0]))
            print("Hall Number is     :%d" % (rec[0][1]))
            print("Hall Name          :%s" % (rec[0][2]))
            print('Customer name is   :%s' % (rec[0][3]))
            print('Seat Type          :%s' % (rec[0][4]))
            print("Number of Seats    :%d" % (rec[0][5]))
            print("Cost per Seat      :%d" % (rec[0][6]))
            print("Discount           :%d" % (rec[0][7]))
            total = rec[0][5]*rec[0][6]-rec[0][7]
            print("Total Cost         :%d" % (total))
            #print(rec)
        else:
            print('Ticket Number not available')

    if choice==7:
        sys.exit(0)
    

    os.system('pause')
    os.system('cls')
