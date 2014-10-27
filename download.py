import mechanize,os,urllib2,urllib,requests,getpass,time
start_time = time.time()
from bs4 import BeautifulSoup
br=mechanize.Browser()
br.open('https://nalanda.bits-pilani.ac.in/login/index.php')
br.select_form(nr=0)
    
name=''
while name=='':
    try:
        print '*******'
        username=raw_input('Enter Your Nalanda Username: ')
        password=getpass.getpass('Password: ')
        br.form['username']=username
        br.form['password']=password
        res=br.submit()
        response=res.read()
        soup=BeautifulSoup(response)
        name=str(soup.find('div',attrs={'class':'logininfo'}).a.string)[:-2]
    except:
        print 'Wrong Password'
f=open('details.txt','w')
f.write(username+'\n'+password)
f.close()
print 'Welcome, '+name
print 'All the files will be downloaded in your Drive C in a folder named "nalanda"'
#print soup.prettify()
div=soup.find_all('div',attrs={'class':'box coursebox'})

l=len(div)
a=[]
for i in range(l):
    d=div[i]
    s=str(d.div.h2.a.string)
    s=s[:s.find('(')]
    c=(s,str(d.div.h2.a['href']))
    path='c:\\nalanda\\'+c[0]
    if not os.path.exists(path):
        os.makedirs(path)
    a+=[c]
#print a
overall=[]
for i in range(l):
    response=br.open(a[i][1])
    page=response.read()
    soup=BeautifulSoup(page)
    li=soup.find_all('li',attrs={'class':'section main clearfix'})
    x=len(li)
    t=[]
    folder=a[i][0]
    print 'Downloading '+folder+' files...'
    o=[]
    for j in range(x):
        g=li[j].ul
        if g!=None:
            if g.li['class'][1]=='resource':
                o+=[j]
                h=li[j].find('div',attrs={'class':'content'})
                s=str(h.h3.string)
                path='c:\\nalanda\\'+folder
                if path[-1]==' ':
                    path=path[:-1]
                path+='\\'+s
                if not os.path.exists(path):
                    os.makedirs(path)
                f=g.find_all('li')
                r=len(f)
                z=[]
                for e in range(r):
                    p=f[e].div.div.a
                    q=f[e].find('span',attrs={'class':'resourcelinkdetails'}).contents
                    link=str(p['href'])
                    text=str(p.find('span').contents[0])
                    typ=''
                    if str(q[0]).find('word')!=-1:
                        typ='.docx'
                    elif str(q[0]).find('JPEG')!=-1:
                        typ='.jpg'
                    else:
                        typ='.pdf'
                    if typ!='.docx':
                        res=br.open(link)
                        soup=BeautifulSoup(res.read())
                        if typ=='.jpg':
                            di=soup.find('div',attrs={'class':'resourcecontent resourceimg'})
                            link=di.img['src']
                        else:
                            di=soup.find('div',attrs={'class':'resourcecontent resourcepdf'})
                            link=di.object['data']
                    try:
                        if not os.path.exists(path+'\\'+text+typ):
                            br.retrieve(link,path+'\\'+text+typ)[0]
                    except:
                        print 'Connectivity Issues'
                    z+=[(link,text,typ)]
                t+=[(s,z)]
    if t==[]:
        print 'No Documents in this subject'
    overall+=[o]
    #raw_input('Press any button to resume')
#print overall
print 'Time Taken to Download: '+str(time.time()-start_time)+ ' seconds'
print 'Do you think you can download all files faster than this :P'
print 'Closing in 10 seconds'
time.sleep(10)
