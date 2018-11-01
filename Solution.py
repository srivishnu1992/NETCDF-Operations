import os                       #To traverse input directory
import netCDF4 as nc4
import numpy as np

inputPath = 'input/'
outputPath = 'output/'
fileNames = os.listdir(inputPath)
files = len(fileNames)
count=0;
for file in fileNames:
	print(str(count)+" out of "+str(files)+" files processed")
	dataFile = nc4.Dataset(inputPath+file, 'r+')
	outputFilename = file[0:6]+'avg'+file[6:]
	outputFile = nc4.Dataset(outputPath+outputFilename, 'w')
	outputFile.createDimension('time', None)
	for att in dataFile.ncattrs():
		outputFile.setncattr(att, dataFile.getncattr(att))
	outputFile.set_auto_mask(False)
	outputFile.createVariable('atmospheric_pressure', 'f4', 'time')
	for att in dataFile['atmos_pressure'].ncattrs():
		outputFile['atmospheric_pressure'].setncattr(att, dataFile['atmos_pressure'].getncattr(att))
	tempVar = outputFile.createVariable('mean_temperature', 'f4', 'time')
	for att in dataFile['temp_mean'].ncattrs():
		outputFile['mean_temperature'].setncattr(att, dataFile['temp_mean'].getncattr(att))
	numpyAtmos = dataFile['atmos_pressure'][:].data
	numpyTemp = dataFile['temp_mean'][:].data
	n = len(numpyAtmos)   
	vals = int(n/5)
	insertAtmos = [None]*vals
	insertTemp = [None]*vals
	for i in range(0,vals):
		insertAtmos[i] = round(np.average(numpyAtmos[i*5:(i*5)+5]),2)
		insertTemp[i] = round(np.average(numpyTemp[i*5:(i*5)+5]),2)
	outputFile['atmospheric_pressure'][:] = insertAtmos
	outputFile['mean_temperature'][:] = insertTemp
	count+=1
print("Completed processing")

def test1():
	testFile1 = nc4.Dataset('output/sgpmetavgE13.b1.20181002.000000.cdf', 'r+')
	temp = testFile1['atmospheric_pressure'][0]
	if str(temp) == str(97.93):
		print("\n Unittest1 Passed")
		assert True
	else:
		assert False
def test2():
	testFile2 = nc4.Dataset('output/sgpmetavgE13.b1.20181003.000000.cdf', 'r+')
	temp = testFile2['mean_temperature'][3]
	if str(temp) == str(28.24):
		print("\n Unittest2 Passed")
		assert True
	else:
		assert False

test1()
test2()

