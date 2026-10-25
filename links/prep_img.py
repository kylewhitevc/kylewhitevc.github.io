"""Studio-normalise still-life product shots: trim the white backdrop, centre on warm paper, multiply so white reads as paper."""
import sys
from PIL import Image, ImageChops
PAPER=(236,229,217)
def studio(src,dst,W=600,H=750,pad=.13,thr=238):
    im=Image.open(src).convert('RGB')
    g=im.convert('L').point(lambda v:255 if v<thr else 0)
    box=g.getbbox() or (0,0)+im.size
    im=im.crop(box)
    mw,mh=W*(1-2*pad),H*(1-2*pad)
    s=min(mw/im.width,mh/im.height); im=im.resize((max(1,int(im.width*s)),max(1,int(im.height*s))),Image.LANCZOS)
    canvas=Image.new('RGB',(W,H),(255,255,255)); canvas.paste(im,((W-im.width)//2,(H-im.height)//2+int(H*.02)))
    out=ImageChops.multiply(canvas,Image.new('RGB',(W,H),PAPER))
    out.save(dst,'WEBP',quality=84,method=6)
if __name__=='__main__':
    studio(sys.argv[1],sys.argv[2])
