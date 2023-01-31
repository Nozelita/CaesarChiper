import math
import sys
import re

g_posR = 0  
g_posC = 0  

g_dirR = 0  
g_dirC = 0  

g_borderL = 0  
g_borderT = 0  
g_borderR = 0  
g_borderB = 0  

grid = []  


def fillTableForEncrypt(letters, totalRows, totalCols):
    """ creates an array to hold the plaintext and appends extra character """
    for number_of_rows in range(math.ceil(len(letters) / totalCols)):
        rows = []  # holds cipher text
        for index in range(totalCols): 
            if number_of_rows * totalCols + index < len(letters):
                rows.append(letters[number_of_rows * totalCols + index])
            else:
                rows.append('-')
        grid.append(rows)  

    return grid  


def fillTableForDecrypt(letters, totalRows, totalCols, pathtype):
    """creates decryption matrix using the ciphertext"""
    global g_posR, g_posC  
    newGrid = []  

    for number_of_rows in range(math.ceil(len(letters) / totalCols)):
        rows = []  
        for index in range(totalCols):
            if number_of_rows * totalCols + index < len(letters):
                rows.append(letters[number_of_rows * totalCols + index])
            else:
                rows.append('-') 
        newGrid.append(rows)  

    initPathParameters(pathtype, totalRows, totalCols)  
    pos = 0  
    while pos < totalRows * totalCols:  
        newGrid[g_posR][g_posC] = letters[pos]
        makeOneStep(pathtype)
        pos += 1  
    
    return newGrid 


def readCipherText(grid, totalRows, totalCols, pathtype):
    """reads the newly created cipher text"""
    initPathParameters(pathtype, totalRows, totalCols)  
    global g_posR, g_posC  
    cipher_text = ""  
    while len(cipher_text) < totalRows * totalCols:
        cipher_text += grid[g_posR][g_posC]
        makeOneStep(pathtype)  
    return cipher_text  


def readPlainText(decryptedGrid, totalRows, totalCols):
    """reads decrypted matrix"""
    plain_text = "" 
    for index in range(totalRows): 
        for element in range(totalCols): 
            plain_text += str(decryptedGrid[index][element]) 
    return plain_text 


def initPathParameters(pathtype, totalRows, totalCols):
    """sets starting positions for searahjarumjam,countersearahjarumjam decryption/encryption"""
    global g_posR, g_posC, g_borderL, g_borderT, g_borderR, g_borderB, g_dirR, g_dirC
    g_posR = 0  
    g_posC = totalCols - 1  

    g_borderL = 0  
    g_borderT = 0  
    g_borderR = totalCols - 1  
    g_borderB = totalRows - 1  

    if pathtype == "searahjarumjam":
        g_dirR = 0  
        g_dirC = -1  

def makeOneStep(pathtype):
    """moves position in grid"""
    global g_posR, g_posC, g_borderL, g_borderT, g_borderR, g_borderB, g_dirR, g_dirC

    if g_posR + g_dirR >= g_borderT and g_posR + g_dirR <= g_borderB:
        g_posR += g_dirR  
    else: 
        if g_dirR == 1: 
            if pathtype == "searahjarumjam": 
                g_dirR = 0  
                g_dirC = 1 
                g_borderL += 1 

        elif g_dirR == -1:
            if pathtype == "searahjarumjam":
                g_dirR = 0 
                g_dirC = -1 
                g_borderR -= 1 

    if g_posC + g_dirC >= g_borderL and g_posC + g_dirC <= g_borderR:
        g_posC += g_dirC 
    else:
        if g_dirC == 1:
            if pathtype == "searahjarumjam":  
                g_dirR = -1 
                g_dirC = 0 
                g_borderB -= 1 
        else:
            if pathtype == "searahjarumjam": 
                g_dirR = 1 
                g_dirC = 0  
                g_borderT += 1 

        g_posR += g_dirR 

def menuCheck(questions):
    """checks input from user and repeats questions if a error is encountered"""
    values = ""  
    while True:
        user_input = input(questions)
        user_input = user_input.replace(" ", "")  
        if len(user_input) == 0 or user_input == "1" or user_input == "0":  
            print("Error! No input detected or insufficient route size. ")
        elif re.match("^[A-Za-z0-9_-]*$", user_input):
            values = user_input  
            break  
    return values  


def grouping(plain_text, totalCols):
    """creates matrix from the plaintext that is used to encrypt and decrypt"""
    if len(plain_text) % totalCols == 0: 
        return [plain_text[rows*totalCols:rows*totalCols+totalCols] for rows in range(len(plain_text)//totalCols)]
    else:  
        return [plain_text[rows*totalCols:rows*totalCols+totalCols] for rows in range(len(plain_text)//totalCols+1)]

def main():
    pathOptions = """Masukan Pilihan :\n[1]. Searah Jarum Jam\n Notes:( Dimulai Dari Kiri Bawah )\n\n>>> """
    routeSizeChoice = "\nJumlah Baris : "
    getPlaintext = "Masukan Teks : "

    while True:
        choice = input(pathOptions)
        if choice == "1": 
            pathtype = "searahjarumjam"
            break 

        else:
            print('Invalid input: Masukan Pilihan\n')

    try:
        route_size = menuCheck(routeSizeChoice) 
        totalCols = int(route_size)  
    except Exception as e: 
        print("A errors has occurred: ",e) 
        print("Rerunning program.........")
        route_size = menuCheck(routeSizeChoice) 

    plain_text = menuCheck(getPlaintext)  
    totalRows = len(plain_text) / totalCols 
 
    if totalRows != math.floor(totalRows): 
        totalRows = math.floor(totalRows) + 1 
    elif type(totalRows) is float: 
        totalRows = len(plain_text) // totalCols 

    new_grid = []

    if choice == "1":
        grid = fillTableForEncrypt(plain_text, totalRows, totalCols) 
        encryptedText = readCipherText(grid, totalRows, totalCols, pathtype) 
        new_grid = fillTableForDecrypt(encryptedText, totalRows, totalCols, pathtype)
        decryptedText = readPlainText(new_grid, totalRows, totalCols)

    if choice == "1":
        print("Enkripsi : ", encryptedText)
        print("Dekripsi : ", decryptedText)

if __name__ == "__main__":
    main()