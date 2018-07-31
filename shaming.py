from selenium import webdriver
import urllib.request
from bs4 import BeautifulSoup
import re
import os
import numpy as np
from PIL import Image

def ImageMerge(files, episode):
    size_x = []
    size_y = []
    file_list = []
    sume = 0


    for file in files:
        image = Image.open(file)
        size_x.append(image.size[0])
        size_y.append(image.size[1])

    
    x_min = min(size_x)
    y_min = min(size_y)
    total_y_size = sum(size_y)

    
    for file in files:
        image = Image.open(file)
        resized_file = image.resize((x_min, image.size[1]))
        file_list.append(resized_file)
    
    
    new_image = Image.new("RGBA", (x_min, total_y_size), (256,256,256,0))
    
    for i in range(0, len(files)):
        area = (0, sume)
        new_image.paste(file_list[i], box = area)
        sume = sume+file_list[i].size[1]
    new_image.save(episode+'.jpg')

def MergeImage(images, episode):
    list_im = images
    print(list_im)
    imgs    = [ Image.open(i) for i in list_im ]

    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)   
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
    
    # save that beautiful picture
    #imgs_comb = Image.fromarray( imgs_comb)
    #imgs_comb.save( 'Trifecta.jpg' )    
    
    # for a vertical stacking it is simple: use vstack
    imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )  
    imgs_comb = Image.fromarray( imgs_comb)
    print(imgs_comb)
    imgs_comb.save( episode+'.jpg' )
    imgs_comb = []
    print(imgs_comb)
    
    

def pageNavigator(driver, url):
    driver.get(url)
    html = driver.page_source
    bsobj = BeautifulSoup(html, "html.parser")
    title = bsobj.find("p", {"class" : "comics-title style-scope comics-horizontal-card"})
    episodeNum = bsobj.findAll("h4", {"class" : "classification"})
    episodeURL = bsobj.findAll("a", {"class" : False, "style" : False, "href" : re.compile("https://manaaspace.net/p/")})


    '''
    #디버그
    #print(title.get_text())
    for i in range(0, len(episodeNum)):
        print(episodeNum[i].text.strip())

    for i in range(0, len(episodeURL)):
        print(episodeURL[i].get('href'))
    #
    '''


    for i in range(3,len(episodeNum)): #len(episodeNum)
        getURL(episodeURL[i].get('href'), episodeNum)





def ImageDown(url, path, i):
    os.chdir("/home/pi/Desktop/collect/"+path)
    

    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    #urllib.request.urlretrieve(url.get('src'), path+" "+url.get('alt')+".jpeg")
    urllib.request.urlretrieve(url.get('src'), "{0:03d}".format(i)+".jpeg")



def getURL(url, episode):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    open_episode = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)
    open_episode.implicitly_wait(2)

    


    open_episode.get(url)


    html = open_episode.page_source

    bsobj = BeautifulSoup(html, "html.parser")
    
    images = bsobj.findAll("img", {"alt" : re.compile("이미지")})
    
    titles = bsobj.find("h1")

    print(len(images))
    
    imagelist = []

    #print(titles.get_text())

    if not os.path.exists(titles.get_text()):
        os.makedirs(titles.get_text())

    print(images[0].get('src'))

    for i in range(0, len(images)):
        print(images[i].get('src'))
        ImageDown(images[i], titles.get_text(), i)
        imagelist.append("{0:03d}".format(i)+".jpeg")

    #MergeImage(imagelist, titles.get_text())
    #ImageMerge(imagelist, titles.get_text())
    imagelist = []
    os.chdir("/home/pi/Desktop/collect/")

    open_episode.close()




# driver = webdriver.Chrome()

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# UserAgent값을 바꿔줍시다!
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

driver2 = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)

#driver.implicitly_wait(2)
driver2.implicitly_wait(2)

pageNavigator(driver2, "https://manaaspace.net/work/vjnMxzWoRbzR3Krw")

driver2.close()

# getURL(driver, 'https://manaaspace.net/p/Qq73REe5G2kMp8jVm48zoOmPXj0By1gv')



