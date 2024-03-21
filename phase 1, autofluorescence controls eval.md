# proof of concept stage, autofluorescence control experiments

author: Daniel Walther
creation date: 2023.03.13
model organism: Xenopus tropicalis
experiment date: recently (last few weeks)

## Expected outcomes of the control series

Both stainings:
- 488 647 (++): very different (stains worked well)
- 488 647: the background signal intensity (of the BABB agarose block) is the same for the two laser channels
- the a5 antibody apparently bound more specifically to its epitome than the Tnnt2 one, as in the Tnnt2 ++ 647 image, the regions of interest (ROI) are clearly brighter than the rest, but not as blindingly much brighter as the respective ROIs in the a5 ++ 647 image.
 - both worked nicely though.

Tnnt2 stain worked
- 488 ++, +-, --: ~= look the same. maybe some more sparkly artefacts~ in the ++ line, but no outstanding differences
- 647 488 (+-, --): ~= but 488 images are a lot brighter!
 -> artefacts outside of the specimens appear brighter in 647 since the specimen is less bright in terms of absolute signal intensity
 => **488 nm is a better excitation wavelength than 647 (/633)** for autofluorescence with the current experimental setup

a5 stain worked
- 488 ++, +-, --: ~=
 - +-: the specimen is quite distorted. its 647 and 488 channels look the same.
 - --: the 647 image shows a gradient of brightness being brighter towards the tadpole's tail. TBD: Compare to the benchtop images (where all 3 embryos of all conditions will be imaged), maybe some shutter artefact, or some specimen specific effect, idk.
- 488 746: ~= same thing with the brightness (488 channel is always brighter)




### Table to fill in for the github documentation repository (TBD - maybe also scrap this part... tidious):

Tnnt2 ++ 488 nm			| Tnnt2 ++ 647 nm		
----------------------------------------------------------------
... | ...
----------------------------------------------------------------
Tnnt2 +- 488 nm			| Tnnt2 +- 647 nm		
----------------------------------------------------------------
... | ...
----------------------------------------------------------------
Tnnt2 -- 488 nm			| Tnnt2 -- 647 nm		
----------------------------------------------------------------
... | ...
----------------------------------------------------------------
a5 ++ 488 nm			| a5 ++ 647 nm			
----------------------------------------------------------------
... | ...
----------------------------------------------------------------
a5 +- 488 nm			| a5 +- 647 nm			
----------------------------------------------------------------
... | ...
----------------------------------------------------------------
a5 -- 488 nm			| a5 -- 647 nm			
----------------------------------------------------------------
... | ...
----------------------------------------------------------------
cas - 488 nm			| cas - 647 nm			
----------------------------------------------------------------
... | ...
----------------------------------------------------------------

