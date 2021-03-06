#!/usr/bin/env python
import sys
import os
import difflib

def decodeSpeech(hmmd,lmdir,dictp,wavfile):
        """
        Decodes a speech file
        """
        try:
                import pocketsphinx as ps
                import sphinxbase
        except:
                print """Pocket sphinx and sphixbase is not installed
                in your system. Please install it with package manager.
                """
        
        speechRec = ps.Decoder(hmm = hmmd, lm = lmdir, dict = dictp)
        wavFile = file(wavfile,'rb')
        wavFile.seek(44)
        speechRec.decode_raw(wavFile)
        result = speechRec.get_hyp()

        return result[0]
def fileTypeFilter(dir):
	filelist = sorted(os.listdir('./test/'))
	filedict = dict([filelist[i:i+2] for i in range(0, len(filelist), 2)])

	return filedict

if __name__ == "__main__":
        hmdir = "/usr/share/pocketsphinx/model/hmm/wsj1/"
        lmd = "/usr/share/pocketsphinx/model/lm/wsj/wlist5o.3e-7.vp.tg.lm.DMP"
        dictd = "/usr/share/pocketsphinx/model/lm/wsj/wlist5o.dic"
        filedict = fileTypeFilter('./test/')
	recognisedSent = list()
	originalSent = list()
	perRatio = list()
	for i in filedict:
            recognised = decodeSpeech(hmdir,lmd,dictd, './test/'+filedict[i])
	    print 'Comparing recognised sentence to origianl one'
            print recognised.lower()
	    recognisedSent.append(recognised.lower())
	    f = file('./test/'+ i, 'rb')
	    original = f.read()[8:-2]
	    print original
	    f.seek(0)
	    f.close()
	    originalSent.append(original.lower())
            perRatio.append(difflib.SequenceMatcher(None, recognised.lower(), original.lower()).ratio())
	print '----------------------------------------------------------------'
	print recognisedSent 
	print '----------------------------------------------------------------'
	print originalSent
        #allRatio = difflib.SequenceMatcher(None, recognisedSent, originalSent).ratio()
	print '----------------------------------------------------------------'
	print 'average ratio:',sum(perRatio)/len(filedict)
	print 'min ratio:', min(perRatio)
	print 'max ratio:', max(perRatio)

