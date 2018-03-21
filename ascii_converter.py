import csv
import unicodedata

nlight = ['F101992', 'F101993', 'F101994', 'F121994', 'F121995', 'F121996', 'F121997', 'F121998', 'F121999', 'F141997', 'F141998', 'F141999', 'F142000', 'F142001', 'F142002', 'F142003', 'F152000', 'F152001', 'F152002', 'F152003', 'F152004', 'F152005', 'F152006', 'F152007', 'F162004', 'F162005', 'F162006', 'F162007', 'F162008', 'F162009', 'F182010', 'F182011', 'F182012', 'F182013']
transform_list = ['bin1_NL_new', 'bin2_NL_new', 'bin3_NL_new', 'bin4_NL_new', 'bin5_NL_new']

for transform in transform_list:

    for x in nlight:

        filename = "BRA_adm2_{}_{}".format(x, transform)
        infile = "/Users/azharhussain/Dropbox/GCP_Reanalysis/RA_Files/Azhar/Nightlights/Income/Data/NL/" + filename + ".csv"
        outfile = "/Users/azharhussain/Dropbox/GCP_Reanalysis/RA_Files/Azhar/Nightlights/Income/Data/NL/" + filename + "_ascii.csv"

        old_data = []
        with open(infile, 'r') as csvfile:
            brazilreader = csv.reader(csvfile, delimiter=',')
            for row in brazilreader:
                old_data.append(row)

        def to_ascii(str):
            return unicodedata.normalize('NFKD', str).encode('ascii', 'ignore').decode('ascii')

        with open(outfile, 'w', newline='') as csvout:
            outwriter = csv.writer(csvout, delimiter=',')
            for row in old_data:
                row = [to_ascii(x) for x in row]
                outwriter.writerow(row)

        print('complete')
