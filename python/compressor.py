import sched, time, os, sys

def callback(sc, impath, nbr):
    sc.enter(20, 1, callback, (sc, impath, nbr+1))
    print "Compressing..."
    temps = []
    counter = 0;
    for f in os.listdir(impath):
        if not os.path.isfile(os.path.join(impath, f)):
            continue
        if f[:5] != "depth":
            continue
        tempname = os.path.join(impath, "tempdepth%d.png" % counter)
        os.rename(os.path.join(impath, f), tempname)
        temps.append(tempname)
        counter += 1
    depthimages = os.path.join(impath, "tempdepth%d.png")
    rgbimages = os.path.join(impath, "temprgb%d.png")
    avconv = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "libav", "bin", "avconv")) # absolute path on others as well?
    os.system("%s -r 30 -i %s -pix_fmt gray16 -vsync 1 -vcodec ffv1 -coder 1 video%d.mov" % (avconv, depthimages, nbr))
    #os.system("../libav/bin/avconv -r 30 -i (IMAGE_FOLDER)/temprgb%06d.tiff -pix_fmt gray16 -vsync 1 -vcodec ffv1 -coder 1 video.mov")
    # avconv -f x11grab -r 15 -s 1366x768 -i :0.0 -c:v libx264 -preset ultrafast -crf 0 test.mkv
    for f in temps:
        os.remove(f)
    #sc.enter(20, 1, callback, (sc, impath, nbr+1)) # possible to schedule it for later irrespective of how long this takes??
# do your stuff

def main(argv):
    s = sched.scheduler(time.time, time.sleep)
    nbr = 0
    s.enter(20, 1, callback, (s, argv, nbr))
    s.run()

if __name__ == "__main__":
    main(sys.argv[1])
