import elt.extract as ext
import elt.load as lo

startDate = input("Enter the first date to collect (YYYY-MM-DD): ")
endDate = input("Enter the last date to collect (YYYY-MM-DD): ")

client = ext.NCEIClient()
jsonData = ext.NCEIClient.fetch(client, startDate, endDate)
ext.NCEIClient.save(client, jsonData)

data = lo.readFilter()
lo.insert(data)