def printHeaderComment(file):
	header = "-- ===================================================================================\n"
	header += "-- ENSURE THIS OUTPUT COMPILES IN SQLSERVER :)\n"
	header += "-- ===================================================================================\n"
	header += "-- Create/Alter Function/Procedure Template\n"
	header += "-- Script Author :\n"
	header += "-- JIRA Ticket :\n"
	header += "-- Version Of This Script : V1.0.0.0\n"
	header += "-- Reason For This Script :\n"
	header += 5 * "--\n"
	header += "-- Known Dependencies : \n"
	header += "--\n"
	header += "-- ===================================================================================\n"
	file.write(header)

def printHeaderDeclare(file, dbName, schemaName, jiraTkt, scriptName, objectName, dropIfExists='0'):
	declare = ""
	declare += "\nDECLARE @dbName VARCHAR(250) = '" + dbName + "'"
	declare += "\nDECLARE @schemaName VARCHAR(250) = '" + schemaName + "'"
	declare += "\nDECLARE @dropIfExists VARCHAR(250) = '" + dropIfExists + "'"
	declare += "\nDECLARE @jiraTkt VARCHAR(250) = '" + jiraTkt + "'"
	declare += "\nDECLARE @scriptName VARCHAR(250) = '" + scriptName + "'"	
	declare += "\nDECLARE @objectName VARCHAR(250) = '" + objectName + "'"	
	declare += "\nDECLARE @spExecuteCode VARCHAR(max) = ''"
	file.write(declare)
	
def printBeginTry(file):
	begintry = ""
	begintry += "\nBEGIN TRY\n"
	file.write(begintry)
	
def printEndTry(file):
	endtry = ""
	endtry += "\nEND TRY\n"
	file.write(endtry)

def printIfObjectExists(file, schemaName, objectName):
	objectExists = ""
	objectExists += "\n  IF OBJECT_ID (N'[" + schemaName + "].[" + objectName + "]') IS NULL"
	objectExists += "\n\n-- object does not exist, proceed to create"
	objectExists += "\n  BEGIN"	
	file.write(objectExists)

def printBegin(file):
	begin = "\nBEGIN\n"
	file.write(begin)
	
def printEnd(file):
	end = "\nEND\n"
	file.write(end)

def printOffsetBegin(file):
	begin = "\n  BEGIN\n"
	file.write(begin)
	
def printOffsetEnd(file):
	end = "\n  END\n"
	file.write(end)

def printElse(file):
	els = "\nELSE\n"
	file.write(els)

def printBeginCatch(file):
	beginCatch="\nBEGIN CATCH\n"
	file.write(beginCatch)

def printEndCatch(file):
	endCatch = "\nEND CATCH\n"
	file.write(endCatch)
	
def printUseDbName(file, dbName):
	useDbName = "\n\nUSE [" + dbName + "]\n"
	file.write(useDbName)
	
def printInCodeCommentText(file, commentText):
	spText = "\n--=============Developer Comments====================================================="
	commentLines = commentText.splitlines()	
	for line in commentLines:
		spText += "\n-- " + line
	spText += "\n--===================================================================================="
	file.write(spText)

def printAnsiText(file):
	spText = "\n"
	spText += "\nSET ANSI_NULLS ON"
	spText += "\n\nSET QUOTED_IDENTIFIER ON\n"
	file.write(spText)
	
def printSpCode(file, spCode):	
	spText = ""
	spText += "\n  DECLARE @spCode VARCHAR(MAX) = N'"
	spQuotedCode = replaceSingleQuoteWithTwoSingleQuotes(spCode)
	spText += "\n  " + spQuotedCode + "'\n"	
	file.write(spText)

def replaceSingleQuoteWithTwoSingleQuotes(spText):
	spText = spText.replace("'","''")
	return spText
	
def printLogCreate(file, objType):
	logText = "\n"
	logText += "\n  PRINT '" + objType + " ' + @dbName + '.' + @schemaName + '.' + @objectName + ' created successfully. ' + @jiraTkt + ' : ' + @scriptName"
	file.write(logText)
	
def printLogReplace(file, objType):
	logText = "\n"
	logText += "\n  PRINT '" + objType + " ' + @dbName + '.' + @schemaName + '.' + @objectName + ' altered successfully. ' + @jiraTkt + ' : ' + @scriptName"
	file.write(logText)

def printExecCode(file, objType, alter):
	execCode = "\n  SET @spExecuteCode = '"
	if alter:
		execCode += "ALTER " + objType +" '" 
	else:
		execCode += "CREATE " + objType + " '"
	execCode += "+ @spCode"
	execCode += "\n  EXEC(@spExecuteCode)\n"
	file.write(execCode)

def printErrorCodeText(file):
	errCodeText = "\n"
	errCodeText += "PRINT 'Errors encountered: ' + CONVERT(VARCHAR(20), ERROR_NUMBER()) + ' Message: ' + ERROR_MESSAGE() + "
	errCodeText += "\n @dbName + '.' + @schemaName + '.' + @objectName + ' : ' + @scriptName + ' : ' + @jiraTkt"
	file.write(errCodeText)

import io

def generateTemplate(sqlscript='', comments='', dbName='', schemaName='', objName='', scriptName='', jiraTkt='', objType=''):
	f = io.StringIO()
	printHeaderComment(f)
	printHeaderDeclare(f, dbName, schemaName, jiraTkt, scriptName, objName)
	printUseDbName(f, dbName)
	printInCodeCommentText(f, comments)
	printAnsiText(f)
	printBeginTry(f)
	spCode = sqlscript
	printSpCode(f, spCode)
	printIfObjectExists(f, schemaName, objName)
	printExecCode(f, objType, False)
	printLogCreate(f, objType)
	printOffsetEnd(f)
	printElse(f)
	printOffsetBegin(f)	
	printExecCode(f, objType, True)
	printLogReplace(f, objType)
	printOffsetEnd(f)
	printEndTry(f)
	printBeginCatch(f)
	printErrorCodeText(f)
	printEndCatch(f)
	contents = f.getvalue()
	f.close()
	return contents
