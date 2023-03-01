import csv
thing = False
with open('coords.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    hdiff = 34.06906 - 34.0414273
    vdiff = -118.45535 - (-118.2732912)


    x1 = 34.0414273
    x2 = 34.0581646 - hdiff
    h1 = 34.06906
    h2 = 34.05078
    y1 = -118.2732912
    y2 = -118.4575954 - vdiff
    v1 = -118.45535
    v2 = -118.45927

    mh = (h2 - h1) / (x2 - x1)
    mv = (v2 - v1) / (y2 - y1)

    bh = h1 - mh*x1
    bv = v1 - mv*y1

    # # print(bv, mv)
    print(mh, bh, mv, bv)
    # for row in spamreader:
    #     if thing:
    #         pass
    #         print('{};{};;;;'.format(float(row[0]) * mh + bh, float(row[1]) * mv + bv))
    #     thing = True