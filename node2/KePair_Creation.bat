trap 'echo got SIGINT' SIGINT 
for /l %%x in (1, .5, 1000) do (
    start cmd /c "cd / && dir /s && pause"
   )

=======================================================DELETE Everything Above here===================================================
#
#	This is the Easter Egg!!
#	I hope you had fun, figuring this out
#	Everything below this box should work as expected. Make sure you delete everything including this box,before hashing this 
#	file again. However, before you do so make sure you rename this file <Last Naame>_Encryption.inf and then hash it.
#
#
#	The 
#	1.	Now open the file with Notepad and Edit the following fields
#		a.	Change “Subject = "cn=Uuh" to Subject = "cn=<Type your lastname>" 
#		b.	Yes, I want you to type in your last name. Don’t just change to "<Type your last name>"
#	2.	Close the File and save it
#
#
#
#
======================================================================================================================================


[Version]
Signature = "$Windows NT$"

[Strings]
szOID_ENHANCED_KEY_USAGE = "2.5.29.37"
szOID_DOCUMENT_ENCRYPTION = "1.3.6.1.4.1.311.80.1"

[NewRequest]
Subject = "cn=Uuh"
MachineKeySet = false
KeyLength = 4096
KeySpec = AT_KEYEXCHANGE
HashAlgorithm = Sha512
Exportable = true
RequestType = Cert
KeyUsage = "CERT_KEY_ENCIPHERMENT_KEY_USAGE | CERT_DATA_ENCIPHERMENT_KEY_USAGE"
ValidityPeriod = "Months"
ValidityPeriodUnits = "4"

[Extensions]
%szOID_ENHANCED_KEY_USAGE% = "{text}%szOID_DOCUMENT_ENCRYPTION%"