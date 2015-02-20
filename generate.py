import random
import string
import subprocess
import os

unif = random.uniform
width = 200
height = 60

gw = 5
gh = 3

# http://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python

def random_distort():
    limit = 5
    pts = []
    for x in range(0, width, width/gw):
        for y in range(0, height, height/gh):
            pts.append((x,y))
            pts.append((x+unif(-limit, limit), y + unif(-limit, limit)))
    s = ' -define shepards:power=3 -distort Shepards "'+ " ".join(["%f,%f"%(pt[0],pt[1]) for pt in pts]) + '" '
    return s

def random_color():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

def easy_string():
    letters = string.digits
    num = random.randint(3,10)
    s = "".join([random.choice(letters) for i in range(num)])
    return s

def random_string():
    letters = 3*string.ascii_lowercase + string.ascii_letters
    if random.random() > .7:
        letters = string.digits
    num = random.randint(3,10)
    s = "".join([random.choice(letters) for i in range(num)])
    return s

fonts = open("fonts.txt").read().strip().split()
def random_font():
    #fonts = ['helvetica', 'times-new-roman', 'georgia', 'courier']
    font = random.choice(fonts)
    return font

def random_blob(center):
    return ' -draw "push graphic-context translate {x},{y} rotate {angle} ellipse 0,0 {w},{h} 0,360 pop graphic-context" '.format(
        angle = random.randint(0, 180),
        x = random.randint(-width/2, width/2) + center,
        y = random.randint(-height/2, height/2) + center,
        h = random.randint(10, 40),
        w = random.randint(10, 40),
    )

def random_mask():
    command = 'convert -size 300x300 xc:none -fill black {blob} {blob2} {blob3} -gravity center -crop {width}x{height}+0+0 +repage -alpha extract -negate mask.png'.format(
        width = width,
        height = height,
        blob = random_blob(300/2),
        blob2 = random_blob(300/2),
        blob3 = random_blob(300/2),
    )
    os.system(command)


def random_wave():
    return " -gravity NorthWest -splice {wave_offset}x0+0+0 -wave {wave_height}x{wave_width} -chop {wave_offset}x0+0+0 ".format(
        wave_height = random.randint(7,15),
        wave_width = random.randint(200,700),
        wave_offset = random.randint(0, 200),
    )

def random_noise():
    return ' -rotate {angle}  -wave {h}x{w}   -rotate -{angle} '.format(
        angle = random.randint(0,180),
        h = random.randint(0,3),
        w = random.randint(3,7),
    )

def random_pad():
    return " -gravity northwest -splice {left}x{top} -gravity southeast -splice {right}x{bottom}".format(
        top = random.randint(0, 40),
        bottom = random.randint(0, 40),
        left = random.randint(0, 140),
        right = random.randint(0, 140),
    )

def random_gravity():
    return random.choice([
        'north',
        'northeast',
        'east',
        'southeast',
        'south',
        'southwest',
        'west',
        'northwest',
    ])

def easy_text_params():
    return " -font {font} -pointsize {size} -kerning {kern} ".format(
        font = random_font(),
        size = 72,
        kern = -7,
    )

def random_text_params():
    return " -font {font} -pointsize {size} -kerning {kern} ".format(
        font = random_font(),
        size = random.randint(70, 90),
        kern = random.randint(-10, -5),
    )

def generate():
    string = random_string()
    filename = '/data/captcha/generated/' + string.lower() + '.png'

    command = 'convert -background "{bg}" -fill "{fg}" {text_params} label:"{string}" {pad} {wave} -resize {width}x{height} -gravity {grav} -extent {width}x{height} {distort} -sample 80% -sample {width}x{height} "{filename}" '.format(
        bg = random_color(),
        fg = random_color(),
        #bg = 'white',
        #fg = 'black',
        text_params = random_text_params(),
        string = string,
        pad=random_pad(),
        noise = random_noise(),
        wave=random_wave(),
        width=width,
        height=height,
        grav = random_gravity(),
        distort=random_distort(),
        filename = filename,
    )
    os.system(command)
    if unif(0,1) > .5:
        random_mask()
        mask = 'convert {filename} -mask mask.png -negate +mask {filename}'.format(
            filename = filename,
        )
        os.system(mask)

def easy():
    string = easy_string()
    filename = '/data/captcha/easy/' + string.lower() + '.png'

    command = 'convert -background "{bg}" -fill "{fg}" {text_params} label:"{string}" -resize {width}x{height} -extent {width}x{height} -sample 80% -sample {width}x{height} "{filename}" '.format(
        bg = 'white',
        fg = 'black',
        text_params = easy_text_params(),
        string = string,
        width=width,
        height=height,
        distort=random_distort(),
        filename = filename,
    )
    os.system(command)


for i in range(1000000):
    print i 
    easy()
