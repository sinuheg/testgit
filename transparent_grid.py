from PIL import Image
im = Image.open('dotted-place-template-aguila.png')
pixelMap = im.load()

img = Image.new( im.mode, im.size)
pixelsNew = img.load()
for i in range(img.size[0]):
    for j in range(img.size[1]):
        if i % 3 in {0, 2} or j % 3 in {0, 2}:
           pixelMap[i,j] = (0,0,0,0)
        pixelsNew[i,j] = pixelMap[i,j]
im.close()
img.show()       
img.save("out.png") 
img.close()