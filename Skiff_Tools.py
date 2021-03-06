# This is a collection of functions to aid in the concatination and formatting
# of data for the poster presented at the 2013 APS DPP conference.  This is 
# meant to be imported into another program and the functions used there.

#B

import sys
import csv


def get_sheet_list(csvfile, sep='c', ws='y'):
        '''NOTE: REQUIRES MODULE csv TO BE IMPORTED BEFOREHAND.
        Opens a csv file and returns a list of lists of the contents in 
        string format.  File operations and exceptions are to be taken care
        of in another function.'''
        print("sep = {}".format(sep))
        print("ws = {}".format(ws))
        sheet_list = []
        if sep == 's':  #   This if/else chain was to get around faults in passing the delimiter character as a variable
           file_reader = csv.reader(csvfile, delimiter=' ')
        elif sep == 't':
           file_reader = csv.reader(csvfile, delimiter='\t')
        else:
           file_reader = csv.reader(csvfile, delimiter=',')
        for row in file_reader:
            tmplst = []
            for i in row:
                if ws[0] == 'y' or ws[0] == 'Y':
                    tmplst.append(i.strip())
            sheet_list.append(tmplst)
        return (sheet_list)

def get_csv(in_file_str=None, sep='c', ws='y', title_line=0):  #  maybe add defaults for filename, sep, ws, title, etc.  then it could be called without interaction
        '''NOTE: REQUIRES MODULES csv AND sys TO BE IMPORTED.
        User interface for selecting csv file and uses get_sheet_list to
        compile list of lists of strings representing the csv file.  Function
        then closes the file and returns the master list.'''
        if in_file_str == None:
            try:
                in_file_str = input("\n CSV file name: ")
                in_file = open(in_file_str, 'r')
            except IOError:
                print("\n {} is a bad file name or was not found.  Please check path.".format(in_file_str))
                sys.exit()
            sep = input("\n Column seperation character? ('c' for comma, 's' for space, 't' for tab, defaults to comma): ")
            ws = input("\n Strip whitespace from entries (defaults to yes)? (y/n): ")
            if ws == '':
                ws = 'y'
            title_line = input("\n Enter the number of title or header lines (default is 0): ")
            if title_line == '':
                title_line = 0
            title_line = int(title_line)
        else:
            try:
                in_file = open(in_file_str, 'r')
            except IOError:
                print("\n {} is a bad file name or was not found.  Please check path.".format(in_file_str))
                sys.exit()
        csv_list = get_sheet_list(in_file, sep, ws)
        in_file.close
        csv_list = csv_list[title_line:]
        return(csv_list)
#       title_line = input("\n Is the first line a title line? (y/n): ")
#       if title_line[0] == 'y' or title_line[0] == 'Y':
#               csv_list = csv_list[1:]
#               return(csv_list)
#       else:
#               return(csv_list)

def get_param(file_name, param):
        '''Pulls a plasma parameter from the param files outputted by the 
        'langmuir_auto' LabView program and returns it as a string.  The 'param'
        parameter for the function should be 2 for Vp, 3 for Ne, or 4 for Te.
        No error protection is built in.'''
        work_file = open(file_name, 'r')
        work_list = work_file.readlines()
        param_out = work_list[int(param)].strip('\nVp=NeT ')
        work_file.close()
        return(param_out)

def get_pressure(pres_raw):
        '''Takes the recorded pressure and translates that into the shorthand
        file name tag used in the file naming nomenclature, returning it as
        a string.'''
        pfl = float(pres_raw)
        if pfl <= 2.00:
                pres_file = '1.82'
        elif 2.00 < pfl < 2.40:
                pres_file = '2.2'
        else:
                pres_file = '2.6'
        return(pres_file)

def set_filename(list_line, path='./'):
        '''Generates the string filename of the appropriate param file for the
        given line of the input csv file.  This function is custom to the 
        idiosyncracies of the 2013 DPP Data Set and should be modified or 
        replaced for future data sets.'''
        pres = get_pressure(list_line[1])
        if int(list_line[0]) <= 205:
                num = list_line[0]
                file = '{}{}E-4torr_{}_LMP_params.txt'.format(path,pres, num)
        elif int(list_line[0]) < 1000:
                num = '0{}'.format(list_line[0])
                file = '{}{}E-4torr_{}_LMP_param.txt'.format(path,pres, num)
        else:
                num = list_line[0]
                file = '{}{}E-4torr_{}_LMP_param.txt'.format(path,pres, num)
        return(file)

def add_param(list, paramnum, path='./'):
        '''For each extant entry in the master list, adds the desired parameter
        value taken from the appropriate param file generated by the 'langmuir
        -auto' LabView program. paramnum should be one of three values:
        6 for Vp, 7 for Ne, 8 for Te.  No error protection is built in.'''
        #path = input("\n Please input path to param files (default is ./): ")
        for i in list:
                file = set_filename(i, path)
                param = get_param(file, paramnum-5)
                i[paramnum] = param
        return(list)

def write_master(list):
        '''NOTE: REQUIRES MODULE csv BE IMPORTED AHEAD OF TIME.
        Takes a list of lists and writes to a csv file.'''
        try:
                out_file_str = input("\n Output CSV file name: ")
                out_file = open(out_file_str, 'w')
        except IOError:
                print("\n {} is a bad file name or there exist insufficient permissions.  Please check path.".format(out_file_str))
                sys.exit()
        label_line_list = ['#num', 'Pressure(E-4 torr)', 'Fd. Power(W)', 'f(MHz)', 'vSWR', 'HP Output(mV)', 'Vp(V)', 'Electron Density(n/cc)', 'Electron Temperature(eV)', 'Ref. Power(W)', 'Plasma Power(eV/cc)', 'Fwd. Power - Ref. Power (W)', 'Plasma Production Power(W)', 'Eff.', 'Cs', 'Debye', 'w^2', 'w']
        label_tag = input("\n Use old label format? (y/n): ")
        if label_tag[0] == 'y' or label_tag[0] == 'Y':
            Skiff_Tools_Spreadsheet_Label_Line_List = label_line_list
        else:
            Skiff_Tools_Spreadsheet_Label_Line_List = add_label(list)
        out_writer = csv.writer(out_file)
        out_writer.writerow(Skiff_Tools_Spreadsheet_Label_Line_List)
        for row in list:
                out_writer.writerow(row)
        out_file.close()
        print('\n File {} has been written.\n\n'.format(out_file_str))
        return(None)

def calc_ref_power(swr, fp):
        '''Calculates the reflected power from the fprward (applied) power and 
        the measured vSWR.  Returns Pref as a string.'''
        swr = float(swr)
        fp = float(fp)
        rp = fp * ((swr+1)/(swr-1))**-2
        rp_str = '{:.2f}'.format(rp)
        return(rp_str)

def add_refP(list, swr_row=4, Fp_row=2):
        '''Takes data array (list of lists) and calls function to calculate
        Pref, then adds a column with that data to the array.'''
        for row in list:
                rp = calc_ref_power(row[swr_row], row[Fp_row])
                row.append(rp)
        print("Added 'Reflected Power'")
        return(list)

def calc_Plasma_Power(Ne, Te):
        '''Calculates the "Plasma Power" from Electron Density (Ne) and Electron
        Temperature (Te) and returns it as a string.'''
        Ne = float(Ne)
        Te = float(Te)
        Pp = Ne*Te
        Pp_str = '{:.2f}'.format(Pp)
        return(Pp_str)

def add_Plasma_Energy(list, Ne_row=7, Te_row=8):
        '''Takes data array (list of lists) and calls a function to calculate
        Pp, then adds a column with that data to the array.'''
        for row in list:
                Pe = calc_Plasma_Power(row[Ne_row], row[Te_row])
                row.append(Pe)
        print("Added 'Plasma Energy Density (NeTe)'")
        return(list)

def add_applied_power(list, Fp_row=2, Rp_row=9):
        '''Reads Forward and reflected power power and returns the difference
        as a string in a new column.'''
        for row in list:
                fp = float(row[Fp_row])
                rp = float(row[Rp_row])
                Pap = fp - rp
                Pap_str = '{:.2f}'.format(Pap)
                row.append(Pap_str)
        print("Added 'Applied Power'")
        return(list)

def calc_lost_power(Ne, Te, R='2.5', Mi='39.9'):
        '''calculate power lost in the plasma absed on plasma parameters and
        physical characteristics in cgs units.  
        LP = 2NeTe(pi)(R**2)(sqrt((3/2)(Te/Mi)))'''
        import math
        Ne = float(Ne)
        Te = float(Te)
        R = float(R)
        Mi = float(Mi)
        lp = (2*Ne*Te*math.pi*(R**2)*(10**6)*math.sqrt((Te)/(Mi)))*(1.602E-19)
        #lp_str = '{:.2f}'.format(lp)
        #return(lp_str)
        return(lp)

def add_Eff(list, Ne_row=7, Te_row=8, R='2.5', Mi='39.9', Fp_row=2):
        '''Calculates lost poser by calling 'calc_lost_power' and efficiency
        then adds both to the working data array (list of lists) as strings.'''
        for row in list:
                LP = calc_lost_power(row[Ne_row], row[Te_row], R, Mi)
                FP = float(row[Fp_row])
                eff = (1-(LP/FP))
                lp_str = '{}'.format(LP)
                eff_str = '{:.6f}'.format(eff)
                row.append(lp_str)
                row.append(eff_str)
        print("Added 'Lost Power' and 'Efficiency'")
        return(list)

def add_Eff_alt(list, Ne_row=7, Te_row=8, R='2.5', Mi='39.9', Fp_row=11):
        '''Calculates lost poser by calling 'calc_lost_power' and efficiency
        then adds both to the working data array (list of lists) as strings.'''
        for row in list:
                LP = calc_lost_power(row[Ne_row], row[Te_row], R, Mi)
                FP = float(row[Fp_row])
                eff = (LP/FP)
                lp_str = '{}'.format(LP)
                eff_str = '{:.6f}'.format(eff)
                row.append(lp_str)
                row.append(eff_str)
        print("Added 'Plasma Production Power' and 'Efficiency'")
        return(list)

def calc_Cs(Te, Z=1, gamma=1, Mi=39.9):
        '''calculates ion sound speed independatly as opposed to as a part of 
        the calc_lost_power function.'''
        Te = float(Te)
        Z = int(Z)
        g = int(gamma)
        Mi = float(Mi)
        Cs = ((g*Z*Te)/(Mi))**0.5
        return(Cs)

def calc_Debye(T, N):
        '''calculates the simplified Debye length as found in NRL p.28'''
        T = float(T)
        N = float(N)
        D = (743)*(T/N)**0.5
        return(D)

def calc_iaDispRel(Cs, Dl, k=1):
        '''Calculates the corrected Ion Acoustic Wave dispursion relation(w**2) 
        as found in Bellan Eq.(4.36).  The wave number defaults to 1.'''
        Cs2 = (float(Cs))**2
        Dl2 = (float(Dl))**2
        k2 = (int(k))**2
        w2 = (k2*Cs2)/(1+(k2*Dl2))
        return(w2)

def add_Cs_Debye_iaDispRel(list, Ne_row=7, Te_row=8, Mi='39.9'):
        '''Calculates Ion Sound Speed, Electron Debye length, and Ion Acoustic
        Wave dispursion relation for each line in the data set and adds the 
        values to the set.  Values set to those expected for the argon plasma
        used in the Skiff lab'''
        for row in list:
                Cs = calc_Cs(row[Te_row])
                D = calc_Debye(row[Te_row], row[Ne_row])
                w2 = calc_iaDispRel(Cs, D)
                Cs_str = '{}'.format(Cs)
                row.append(Cs_str)
                D_str = '{}'.format(D)
                row.append(D_str)
                w2_str = '{}'.format(w2)
                row.append(w2_str)
                w = w2**0.5
                w_str = '{}'.format(w)
        print("Added 'Ion Sound Speed', 'Electron Debye Length', 'Ion Acoustic Wave Dispursion Relation (w^2)', and 'w'")
        return(list)

def clean_spect(list):
    '''takes a list generated from the CSV output file from the Ocean Optics 
    SpectraSuite software and converts it to a true CSV, retaining headers.'''

def add_label(list):
    '''interface to add a label/column headers to a csv file '''
    j = 0
    while j<len(list[1]):
        print("Col{}".format(j+1), end='\t')
        j += 1
    j = 0
    print ("\n")
    while j<len(list[1]):
        print('{}'.format(list[1][j]), end='\t')
        j += 1
    label_list = []
    j = 0
    print('\n')
    while j<len(list[1]):
        col = input("Label for Col{}:  ".format(j+1))
        label_list.append(col)
        j += 1
    print ("\n")
    return(label_list)

def compare_lists(list1, list2, compcol, header='n'):
    '''compared a given column in two two-column lists and returns the difference.
    Provisions are made for a header line; further developments are needed to 
    generalize the lists and provide more flexible output of the difference.
    At present, the first column of each list is assumed to be identical and act as
    a key for the reminder of each row.'''
    if header == 'y' or header == 'Y':
        list1 = list1[1:]
        list2 = list2[1:]
#    wl1 = list1[1:]
#    wl2 = list2[1:]
    complst = []
    counter = 0
    for i in list1:
        linelst = []
        linelst.append(list1[counter][0])
        tmp = float(list1[counter][compcol-1]) - float(list2[counter][compcol-1])
        linelst.append(abs(tmp))
        complst.append(linelst)
        counter += 1
    return(complst)

def colswap(list, col1, col2):
    '''Swaps the positions of two columns of a list of lists. '''
    col1 = int(col1)
    col2 = int(col2)
    for i in list:
        tmpa = i[col1]
        i[col1] = i[col2]
        i[col2] = tmpa
    return(list)

def temp_correct(Tb, Eeff=0.386, wl=650):
    '''use to correct the blackbody temperature of a filament based on the observed
    temperature and correcting for emissivity of the emitting body.  Used primarily
    to find correct filament temperature for a tungsten bulb when calibrating the 
    Ocean Optics Spectrometer for use in energy analysis.  Default effective 
    emissivity based on base emissivity for tungsten, corrected for reflection of 
    glass envelope.  Default wavelength based on the wl used in the L&C pyro-
    meter used to determine observed temperature, Tb.  All units are SI. wl is in
    nanometers; Tb and T are in Kelvin.  Eeff is unitless.'''
    h = 6.626E-34
    k = 1.381E-23
    c = 2.99E8
    wl = wl/1E9
    import math
    T = (wl*k*math.log(1+Eeff))/(h*c) + 1/Tb
    T = 1/T
    return(T)

def Ephoton_calc(wl, c=2.997E8):
    '''Caclulates energy of a single photon at the given wavelength(m).  Allunits SI '''
    h = 6.626E-34
    E = h*c/wl
    return(E)

def add_Ephoton(list, col = 0):
    '''takes a list generated from a csv file of the spectrograph and calculates
    the energy of a single photon of the wavelength listed for the channel on 
    each line.  This energy is then appended as an additional column in the list.'''
    for i in list:
        Eph = Ephoton_calc(float(i[col]))
        i.append(Eph)
    return(list)

def sum_energy(list, colwl=0, colcnt=1, scale=1):
    '''Calculates the sum of the energy represented by the counts as measured on
    the spectrograph.  This is done by first calculating as if one count equaled
    one photon of that energy and then applying a scaling factor (photons/count)
    to the final sum of all channels.'''
    sum = 0
    for i in list:
        sum += Ephoton_calc(float(i[colwl])) * float(i[colcnt])
    sum = sum * scale
    return(sum)

#END
