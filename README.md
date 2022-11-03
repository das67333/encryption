Tested on Windows  

Before launch:  
  pip install requests, tk, pillow  

Text mode:  
  Run src/textUI.py with arguments below to encrypt/decrypt the file:  
  -h, --help            show this help message and exit  
  -f FILE, --file FILE  path to the data file  
  -k KEY, --key KEY     encryption/decryption key  
  -c {caesar,vigenere,vernam,custom}, --cipher {caesar,vigenere,vernam,custom}  
                        cipher type to use  
  -e, --encrypt         encrypt the file  
  -d, --decrypt         decrypt the file  
  
Graphical mode:  
  Run src/graphUI.pyw  
  Tab 'Cryptography':  
    Data and key can be entered or given as a file  
    Checkbutton 'hex' converts string<->hex if possible  
    
  Tab 'Steganography':  
    Entry 'Message' is used to enter and to reveal message  
    Original image can be obtained from a link or as a file  
    Edited image always has a 'bmp' extension  
