#Importing the required libraries and modules
import sys;
import json
import MolDisplay; 
import molsql; 
import urllib;
import molecule;
import os
from os.path import join
from http.server import HTTPServer, BaseHTTPRequestHandler;
#port 58356
newDB = molsql.Database(reset=False)
newDB.create_tables()
class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        #When the path / is requested it presents the webform 
        if self.path == "/":
            self.send_response( 200 ); #OK signal since everthing is fine
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(home_page) );
            self.end_headers();
            self.wfile.write( bytes( home_page, "utf-8" ) );
        elif self.path == "/next.html":
            self.send_response( 200 ); #OK signal since everthing is fine
            fp = open ("next.html", "r")
            content = fp.read()
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(content) );
            self.end_headers();
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close()
        elif self.path == "/index.html":
            self.send_response( 200 ); #OK signal since everthing is fine
            fp = open ("index.html", "r")
            content = fp.read()
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(content) );
            self.end_headers();
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close()
        #Otherwise it generates a 404 error
        elif self.path == "/script.js":
            self.send_response( 200 ); #OK signal since everthing is fine
            self.send_header( "Content-type", "text/javascript" );
            file = open("script.js", "r");
            jqueryContent = file.read()
            file.close()
            self.send_header( "Content-length", len(jqueryContent) );
            self.end_headers();
            self.wfile.write( bytes( jqueryContent, "utf-8" ) );
        elif self.path == "/style.css":
            self.send_response( 200 ); #OK signal since everthing is fine
            self.send_header( "Content-type", "text/css" );
            file = open("style.css", "r");
            cssContent = file.read()
            file.close()
            self.send_header( "Content-length", len(cssContent) );
            self.end_headers();
            self.wfile.write( bytes( cssContent, "utf-8" ) );
        elif self.path == "/information":
            self.send_response( 200 );
            self.send_header( "Content-type", "text/html" );
            cursor = newDB.connect.cursor(); 
            cursor.execute("""SELECT Elements.ELEMENT_NAME FROM Elements""" )
            data = cursor.fetchall()
            data = str(data)
            data = data.replace("[", "")
            data = data.replace("]", "")
            data = data.replace("(", "")
            data = data.replace(")", "")
            data = data.replace(",", "")
            data = data.replace("'", "")
            self.send_header( "Content-length", len(data) );
            self.end_headers();
            self.wfile.write(bytes(data, "utf-8"))
        elif self.path == "/infoEcode":
            self.send_response( 200 );
            self.send_header( "Content-type", "text/html" );
            cursor = newDB.connect.cursor(); 
            cursor.execute("""SELECT Elements.ELEMENT_CODE FROM Elements""" )
            data = cursor.fetchall()
            data = str(data)
            data = data.replace("[", "")
            data = data.replace("]", "")
            data = data.replace("(", "")
            data = data.replace(")", "")
            data = data.replace(",", "")
            data = data.replace("'", "")
            self.send_header( "Content-length", len(data) );
            self.end_headers();
            self.wfile.write(bytes(data, "utf-8"))
        elif self.path == "/MolExistOrNot":
            self.send_response( 200 );
            self.send_header( "Content-type", "text/html" );
            cursor = newDB.connect.cursor(); 
            cursor.execute("""SELECT Molecules.NAME FROM Molecules""" )
            data = cursor.fetchall()
            data = str(data)
            data = data.replace("[", "")
            data = data.replace("]", "")
            data = data.replace("(", "")
            data = data.replace(")", "")
            data = data.replace(",", "")
            data = data.replace("'", "")
            self.send_header( "Content-length", len(data) );
            self.end_headers();
            self.wfile.write(bytes(data, "utf-8"))
        elif self.path == "/atomandbondNum":
            self.send_response( 200 );
            self.send_header( "Content-type", "text/html" );
            cursor = newDB.connect.cursor(); 
            cursor.execute("""SELECT Molecules.NAME FROM Molecules""" )
            data = cursor.fetchall()
            data1 =""
            for i in range (len(data)):
                data[i] = str(data[i])
                data[i] = data[i].replace("[", "")
                data[i] = data[i].replace("]", "")
                data[i] = data[i].replace("(", "")
                data[i] = data[i].replace(")", "")
                data[i] = data[i].replace(",", "")
                data[i] = data[i].replace("'", "")
                returnMol = newDB.load_mol(data[i])
                data1 += data[i] 
                data1 += " "
                data1 += str(returnMol.atom_no)
                data1 += " "
                data1 += str(returnMol.bond_no)
                data1 += "\n"
            self.end_headers()
            self.wfile.write( bytes( data1, "utf-8" ) );
        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );
            
    def do_POST (self):
        #When the path /molecule is requested send an svg file to the client 
        if self.path == "/molecule":
            self.send_response( 200 ); # OK signal since everthing is fine
            MolDisplay.radius = newDB.radius()
            MolDisplay.element_name = newDB.element_name()
            MolDisplay.header += newDB.radial_gradients()
            content_length = int(self.headers.get('Content-Length'))
            #Get the length of the user request so we know how much to read in
            body = self.rfile.read(content_length)
            #Convert the file informatioin so that the proper text will be showed up on the webpage
            conversion = body.decode("utf-8")
            #Skip the 4 lines of header information
            conversion = conversion.split ('\n', 4)[4]
            #Need to create a file and write to it so we can parse it later on using P3 code    
            file = open ("user.txt", "w")
            file.write(conversion)
            #Make file back to read mode to we can parse it
            file = open ("user.txt", "r")
            #Creating a molecule object
            newMol = MolDisplay.Molecule()
            #Calling the parse function on the file created and sorting it
            newMol.parse(file)
            newMol.sort()
            #Svg method is called on the molecule to get the returned string
            svgInfo = newMol.svg()
            file.close()
            #Prints the final svg image to the user
            self.send_header("Content-type", "image/svg+xml");
            self.send_header("Content-length", len(svgInfo));
            self.end_headers();
            self.wfile.write( bytes(svgInfo,"utf-8"));
        #Otherwise it generates a 404 error 
        elif self.path == "/Xrotate":
            self.send_response( 200 );
            MolDisplay.radius = newDB.radius()
            MolDisplay.element_name = newDB.element_name()
            MolDisplay.header += newDB.radial_gradients()
            content_length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_length)
            postvars = urllib.parse.parse_qsl( body.decode( 'utf-8' ) );
            mol = newDB.load_mol(postvars[1][1])
            mol.sort()
            mx = molecule.mx_wrapper(int(postvars[0][1]),0,0);
            mol.xform( mx.xform_matrix );
            mol.sort()
            stringSvg = mol.svg()
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(stringSvg));
            self.end_headers(); 
            self.wfile.write( bytes(stringSvg,"utf-8"));
            MolDisplay.radius = ""
            MolDisplay.element_name = ""
            MolDisplay.header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""
        elif self.path == "/Yrotate":
            self.send_response( 200 );
            MolDisplay.radius = newDB.radius()
            MolDisplay.element_name = newDB.element_name()
            MolDisplay.header += newDB.radial_gradients()
            content_length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_length)
            postvars = urllib.parse.parse_qsl( body.decode( 'utf-8' ) );
            mol = newDB.load_mol(postvars[1][1])
            mol.sort()
            mx = molecule.mx_wrapper(0,int(postvars[0][1]),0);
            mol.xform( mx.xform_matrix );
            mol.sort()
            stringSvg = mol.svg()
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(stringSvg));
            self.end_headers(); 
            self.wfile.write( bytes(stringSvg,"utf-8"));
            MolDisplay.radius = ""
            MolDisplay.element_name = ""
            MolDisplay.header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""
        elif self.path == "/Zrotate":
            self.send_response( 200 );
            MolDisplay.radius = newDB.radius()
            MolDisplay.element_name = newDB.element_name()
            MolDisplay.header += newDB.radial_gradients()
            content_length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_length)
            postvars = urllib.parse.parse_qsl( body.decode( 'utf-8' ) );
            mol = newDB.load_mol(postvars[1][1])
            mol.sort()
            mx = molecule.mx_wrapper(0,0,int(postvars[0][1]));
            mol.xform( mx.xform_matrix );
            mol.sort()
            stringSvg = mol.svg()
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(stringSvg));
            self.end_headers(); 
            self.wfile.write( bytes(stringSvg,"utf-8"));
            MolDisplay.radius = ""
            MolDisplay.element_name = ""
            MolDisplay.header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""
        elif self.path == "/mol":
            self.send_response( 200 );
            MolDisplay.radius = newDB.radius()
            MolDisplay.element_name = newDB.element_name()
            MolDisplay.header += newDB.radial_gradients()
            content_length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_length)
            postvars = urllib.parse.parse_qsl( body.decode( 'utf-8' ) );
            mol = newDB.load_mol(postvars[0][1])
            mol.sort()
            stringSvg = mol.svg()
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(stringSvg));
            self.end_headers(); 
            self.wfile.write( bytes(stringSvg,"utf-8"));
            MolDisplay.radius = ""
            MolDisplay.element_name = ""
            MolDisplay.header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""
        elif self.path =="/add":
            self.send_response( 200 );
            content_length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_length)
            conversion = body.decode("utf-8")
            Elementinfo = json.loads(conversion) 
            newDB['Elements']=(Elementinfo['Enum'], Elementinfo['Ecode'], Elementinfo['Ename'], Elementinfo['C1'], Elementinfo['C2'], Elementinfo['C3'], Elementinfo['rad'])
            self.end_headers();
        elif self.path == "/delete":
            self.send_response( 200 );
            content= int(self.headers.get('Content-Length'))
            b = self.rfile.read(content);
            convert = b.decode("utf-8")
            newDB.connect.execute("""DELETE FROM Elements WHERE Elements.ELEMENT_NAME = '%s' """%(convert))
            self.end_headers()
        elif self.path == "/UploaduserMol":
            self.send_response( 200 );
            content= int(self.headers.get('Content-Length'))
            b = self.rfile.read(content);
            convert = b.decode("utf-8")
            Elementinfo = json.loads(convert) 
            lookfor = Elementinfo['fileName']
            for root, dirs, files in os.walk('/home/undergrad/1/ndesai04/cis2750'):
                if lookfor in files:
                 # found one!
                    path = os.path.join(root,lookfor)
                    #print(path) #this is the path you required
            fp = open (path)
            newDB.add_molecule(Elementinfo['userVal'], fp)
            self.end_headers()
        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );



file = open("index.html", "r"); 
home_page=file.read()
file.close()

#Command line argument that allows the user to specify the port of the webserver
httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
httpd.serve_forever()