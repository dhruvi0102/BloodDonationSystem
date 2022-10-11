**Topic: Blood Donation and Requirement System**

**Team members:**
1.	Dhruvi Bavaria (002767470)
2.	Avani Kala (002772623)

The aim of developing the ‘Blood Donation and Requirement System’ database is to keep a track of acceptors and donors in blood banks. This database will be useful to person who is in requirement of blood. Hospitals will also be able to take advantage of this database in case of blood need and contact respective blood banks. 

**Initial Tables and their attributes:**

•	Person: Person_id, firstname, lastname, address, zipcode, contact

•	Donors: donor_id, pid, blood_type, weight, height, gender, DonationDate, AmountDonated, BloodBankID

•	Patients: patient_id, pid, blood_type, Weight, Height, Transfusion Date, BloodBankID

•	Pre-Exam: Peid, pid, hemoglobin, bloodPressure, pulseRate

•	BloodBank: BloodBank_id, Name, Address, Contact, Email, operating_hours

•	BloodBags: BBID, blood_bank_id , BloodType, Quantity

**Explanation of Tables:**

The Person table contains all the people and their information. Two categories include: Donor, Patient. 

The Donor table contains the information required to be a donor. 

The Patient table contains all the patients and their information required before a blood transfusion. 

The Pre_exam table contains the respective information about a donor before a donation, as well as a patient before a transfusion. 

The BloodBanks table contains information of Blood banks location and it’s other information. 

The BloodBags table contains information regarding availability of blood at particular Blood Bank.

**End users:** Person requiring blood, hospitals.
