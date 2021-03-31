# Password generator
    usage: pg.py [-h] [-c] [-a] [-m] [-v] [-V] [-t] [-s SET]



    optional arguments:
    -h, --help         show this help message and exit
    -c , --chars       Length of password in characters (default: 14)
    -a , --amount      Amount of passwords (default: 1)
    -m , --manual      Manual slice set of chars (default: 0)
    -v, --verbose      Show set of chars before generation (default: False)
    -V, --version      Show version (default: False)
    -t, --temporary    Generate temporary password. Ignore all other settings except of -a. Example: Zyx51534 (default: False)
    -s SET, --set SET  Charset for password generation(d: digits, l: lowercase letters, u: uppercase letters, p: punctuation) (default: dlu)

 
Generate 10 "temporary" passwords:

        $./pg.py -t -a10 -v

        Generate temporary password like: Abc12345
        1       Goh38285
        2       Zac99013
        3       Uoi08574
        4       Ool43134
        5       Voc65229
        6       Qet58029
        7       Zum62774
        8       Nog42975
        9       Eou74597
        10      Wei22545

The manual slice set:
        
        
        $./pg.py -c100 -sd -m2

                1001010100110110000101110001111111100011110011100001011001100110000001000100100110110110000011101101


        $./pg.py -c32 -a5 -sdu -m16 -v

        Sliced set(16): 0123456789ABCDEF

        1       04BD2DC646D146C373AD1D126182E3AE
        2       8A996F1E3330218D76EB038D858A8F08
        3       A6CA2EA5C9D40D371E0A3CE83C3F8C29
        4       EE7364236F40622C846E675A6F9B5EA6
        5       848A20F3C7647384FAC8DF3FD7B17E71

        $./pg.py -c32 -a5 -sdl -m16 -v

        Sliced set(16): 0123456789abcdef

        1       e46aa91316dc885082bfe4da1348c0c5
        2       1e69ec02eb0872cb2fbc04082f9b03ec
        3       0644d2857133a76d419ccff49616d589
        4       a221994db3fcc5b0c3a1130685e4db82
        5       fff37974bc27871b8ea91cd0ddfde282

Make sets:
        
        $./pg.py -sdlup -v

        Sliced set(88): 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+,-.:;<=>?@[]^_{}~

        *XJ?-AG7sSNIKY

        