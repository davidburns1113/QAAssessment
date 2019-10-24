from tkinter import *
import datetime as dt
from tabulate import *

class Account(object):
	# Defines an individual account and the methods required for deposits and withdrawals.
	def __init__(self,name,type,address,balance=0,year=dt.date.today().year,password='password'): # Open with empty balance, use current year as year unless specified otherwise.
		input=name.split(' ') # Obtain seperate words of name
		serialdigits=[input[0][0],input[-1][0]] # Obtain initials, ignoring middle name entries
		self.serial=type+serialdigits[0]+serialdigits[1]+str(year) # output serial number
		# This serial structure has a lot of room for duplicate serials. Check that isn't happening.
		for i in data.accounts:
			if i.serial==self.serial:
				# Use increasing digit to denote duplicates - C1AA2019, C2AA2019 etc.
				try:
					insert=int(i.serial[1])
					self.serial=type+str(insert+1)+serialdigits[0]+serialdigits[1]+str(dt.year)
				except:
					self.serial=type+'1'+serialdigits[0]+serialdigits[1]+str(dt.year)
		# Save useful information
		self.holder=name
		self.address=address
		self.balance=balance
		self.history=[]
		self.password=password
			
	def deposit(self,amount): # Deposit money into an account - adding to the deposits table is managed in the GUI section.
		self.balance=self.balance+amount
		self.history.append('+'+str(amount))
		
	def withdraw(self,amount): # Withdraw money from an account - adding to the withdrawals table is managed in the GUI section.
		if self.balance>=amount: # Ensure there is enough money to withdraw.
			self.balance=self.balance-amount
			self.history.append('-'+str(amount))
			return 1
		else:
			return 0
			
class Database(object):
	# Defines the database with a list of Account objects, and a list of lists for deposits and withdrawals.
	def __init__(self,accounts=[],deposits=[],withdrawals=[]): # Constructor
		self.accounts=accounts
		self.deposits=deposits
		self.withdrawals=withdrawals
	
	def add(self,obj,type): # Ensures that the right type of object ends up in the right table.
		if type=='account':
			self.accounts.append(obj)
		elif type=='deposit':
			self.deposits.append(obj)
		else:
			self.withdrawals.append(obj)
		
	def read(self,serial): # Obtains information.
		for i in self.accounts:
			if i.serial==serial:
				return [i.holder,i.serial,i.balance]
				
		
class Interface(object): # Useful for storing application status - mostly used to determine whether to show Login or Account Information panels.
	def __init__(self):
		self.currentuser=[]
# Setup
# Set up a few accounts to fill the database at the start - useful for testing reports without adding accounts first.
# Will also use this to test the duplicate serial and to ensure two people at the same address can have separate accounts (or one person with two accounts.)
data=Database()
inf=Interface()
a1=Account('Name One','C','1 Example Street')
a2=Account('Name Two','C','44 Example Avenue')
a3=Account('Name Three','S','23 Example Street')
a4=Account('Name Four','S','23 Example Street')
a5=Account('Name Five','C','101 Example Mansions')
a6=Account('Name Five','S','101 Example Mansions')
admin=Account('admin','S','Bank of Bank',password='admin')
admin.password='admin'
data.add(a1,'account')
data.add(a2,'account')
data.add(a3,'account')
data.add(a4,'account')
data.add(a5,'account')
data.add(a6,'account')
data.add(admin,'account')
# GUI Basics and Main Screen
gui=Tk()
# Introductory Text
status=Text(gui,height=2,width=30)
status.insert(INSERT,'Please Select Option')
status.pack()
# Button Function Definitions
def gui_newaccount(): # Opens New Account Screen
	newaccountwindow=Toplevel(gui)
	name=Label(newaccountwindow,text="Name")
	nameentry=Entry(newaccountwindow) # Entry for user name.
	address=Label(newaccountwindow,text="Address")
	addressentry=Entry(newaccountwindow)  # Entry for user address.
	typetext=Label(newaccountwindow,text="Account Type")
	types=['C','S']
	type=StringVar(newaccountwindow)
	type.set(types[0])
	typeentry=OptionMenu(newaccountwindow,type,*types) # Dropdown menu for account type.
	password=Label(newaccountwindow,text="Password")
	passentry=Entry(newaccountwindow) # Entry for user password.
	# Pack all elements.
	name.pack()
	nameentry.pack()
	address.pack()
	addressentry.pack()
	typetext.pack()
	typeentry.pack()
	password.pack()
	passentry.pack()
	def create_account(): # Adds the new account as defined by the entries to the accounts table.
		account=Account(nameentry.get(),type.get(),addressentry.get(),balance=0,year=dt.date.today().year,password=passentry.get())
		data.add(account,'account')
		newaccountwindow.destroy() # Close New Account Screen
	# Define and Pack Button with above command.
	create=Button(newaccountwindow,text="Create Account",command=create_account)
	create.pack()
	ret=Button(newaccountwindow,text="Return",command=newaccountwindow.destroy) # Button to close window.
	ret.pack()

	
def gui_login(): # Opens Login Screen
	loginwindow=Toplevel(gui)
	name=Label(loginwindow,text="Name")
	nameentry=Entry(loginwindow) # Entry for user name.
	password=Label(loginwindow,text="Password")
	passentry=Entry(loginwindow) # Entry for user password
	name.pack()
	nameentry.pack()
	password.pack()
	passentry.pack()
	def attempt_login(): # Checks username and password against the database for a match.
		for i in data.accounts:
			if i.holder==nameentry.get(): # Check for name similarity
				if i.password==passentry.get(): # Check for matching password
					inf.currentuser=i # Logs in
					break
		# Reset the GUI to show the options for a logged in user.
		if inf.currentuser!=[]:
			gui=Tk()
			gui.withdraw()
			status=Text(gui,height=2,width=30)
			status.insert(INSERT,'Please Select Option')
			status.pack()
			logout.pack()
			if inf.currentuser.holder=='admin':
				report.pack()
			else:
				#logout.pack()
				account.pack()
				deposit.pack()
				withdraw.pack()
			# Remove buttons not necessary for a logged in user.
			newaccount.pack_forget()
			login.pack_forget()
			loginwindow.destroy() # Close Login screen.
	login1=Button(loginwindow,text="Login",command=attempt_login)
	login1.pack()
	ret=Button(loginwindow,text="Return",command=loginwindow.destroy) # Button to close window.
	ret.pack()

	
def gui_deposit(): # Opens Deposit Screen
	depositwindow=Toplevel(gui)
	deposit=Label(depositwindow,text="Deposit Amount:")
	depositentry=Entry(depositwindow) # Entry for amount to be deposited
	deposit.pack()
	depositentry.pack()
	def makedeposit(): # Try loop to ensure a number is being added.
		try:
			inf.currentuser.deposit(int(depositentry.get()))
			data.add([inf.currentuser.serial,int(depositentry.get())],'deposit')
			depositwindow.destroy() # Closes Deposit screen ONLY on successful transaction.
		except:
			print("Cannot deposit a non-number value.")
		
	makedep=Button(depositwindow,text="Make Deposit",command=makedeposit)
	makedep.pack()
	ret=Button(depositwindow,text="Return",command=depositwindow.destroy) # Button to close window.
	ret.pack()


def gui_withdraw(): # Opens withdrawal screen.
	withdrawwindow=Toplevel(gui)
	withdraw=Label(withdrawwindow,text="Withdraw Amount:")
	withdrawentry=Entry(withdrawwindow) # Entry for withdrawal amount
	withdraw.pack()
	withdrawentry.pack()
	def makewithdraw(): # Try loop ensures a number is added.
		try:
			# If statement ensures that the withdrawal was successful, as if the withdrawal is greater than the balance Withdraw returns 0.
			if inf.currentuser.withdraw(int(withdrawentry.get()))==1:
				data.add([inf.currentuser.serial,int(withdrawentry.get())],'withdraw')
				withdrawwindow.destroy() # Close window ONLY on successful withdrawal.
			else:
				pass
		except:
			print("Cannot withdraw a non-number value.")
		
	makewith=Button(withdrawwindow,text="Make Withdraw",command=makewithdraw)
	makewith.pack()
	ret=Button(withdrawwindow,text="Return",command=withdrawwindow.destroy) # Button to close window.
	ret.pack()


def gui_report(): # Generates reports into the Console.
	reportwindow=Toplevel(gui)
	adminstatus=Text(reportwindow,height=2,width=30)
	adminstatus.insert(INSERT,"Please select a report type.")
	def fullreport(): # Generates reports for all accounts in easy to read table.
		tabulater=[['Serial Number','Account Holder','Address','Balance']]
		for i in data.accounts:
			tabulater.append([i.serial,i.holder,i.address,i.balance])
		print(tabulate(tabulater))
	def savingreport(): # As Fullreport, but if check ensures only Savings Accounts are shown.
		tabulater=[['Serial Number','Account Holder','Address','Balance']]
		for i in data.accounts:
			if i.serial[0]=='S':
				tabulater.append([i.serial,i.holder,i.address,i.balance])
		print(tabulate(tabulater))
	def currentreport(): # As Fullreport, but if check ensures only Current Accounts are shown.
		tabulater=[['Serial Number','Account Holder','Address','Balance']]
		for i in data.accounts:
			if i.serial[0]=='C':
				tabulater.append([i.serial,i.holder,i.address,i.balance])
		print(tabulate(tabulater))
	def indireport(): # Takes input from indentry, then draws a table with the information for all accounts with a holder matching the user entry.
		tabulater=[['Serial Number','Account Holder','Address','Balance']]
		for i in data.accounts:
			if i.holder==indentry.get():
				tabulater.append([i.serial,i.holder,i.address,i.balance])
		print(tabulate(tabulater))
	# Define buttons
	allreport=Button(reportwindow,text='Full Report',command=fullreport)
	savingreport=Button(reportwindow,text='Savings Accounts Report',command=savingreport)
	currentreport=Button(reportwindow,text='Current Accounts Report',command=currentreport)
	individualreport=Button(reportwindow,text='Individual Report',command=indireport)
	indentry=Entry(reportwindow) # Entry for individual holder account reports.
	# Pack all
	adminstatus.pack()
	allreport.pack()
	savingreport.pack()
	currentreport.pack()
	individualreport.pack()
	indentry.pack()
	ret=Button(reportwindow,text="Return",command=reportwindow.destroy) # Button to close window.
	ret.pack()
		
	
def gui_accountstatus(): # Simple screen to display account information for a logged in user.
	accountwindow=Toplevel(gui)
	accstatus=Text(accountwindow,height=2,width=15)
	accstatus.insert(INSERT,inf.currentuser.holder+'\n') # Displays name
	accstatus.insert(INSERT,inf.currentuser.serial+'\n') # Displays serial number
	accstatus.insert(INSERT,inf.currentuser.balance) # Displays balance
	accstatus.pack()
	ret=Button(accountwindow,text="Return",command=accountwindow.destroy) # Button to close window.
	ret.pack()
	
def gui_logout(): # Does not open new screen or dialogue.
	# Simply resets the user interface to show the login and new account options, forgetting all others, and sets the active user to the null state.
	inf.currentuser=[]
	gui=Tk()
	gui.withdraw()
	status=Text(gui,height=2,width=30)
	status.insert(INSERT,'Please Select Option')
	status.pack()
	newaccount.pack()
	login.pack()
	account.pack_forget()
	deposit.pack_forget()
	withdraw.pack_forget()
	report.pack_forget()
	logout.pack_forget()
	
# Pack relevant buttons onto GUI (this has to be done here or it will return Error: commands called before definition.)
newaccount=Button(gui,text="New Account",command=gui_newaccount)
login=Button(gui,text="Login",command=gui_login)
deposit=Button(gui,text="Make a Deposit",command=gui_deposit)
withdraw=Button(gui,text="Make a Withdrawal",command=gui_withdraw)
report=Button(gui,text="Generate Report",command=gui_report)
account=Button(gui,text="Account Status",command=gui_accountstatus)
logout=Button(gui,text="Logout",command=gui_logout)

# Pack buttons required for initial state.
newaccount.pack()
login.pack()

# Run Program.
gui.mainloop()