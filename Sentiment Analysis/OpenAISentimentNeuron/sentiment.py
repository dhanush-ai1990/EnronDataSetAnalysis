from encoder import Model
model=Model()
#text = ['I do not disagree that we may end up in a bad place']
"""
text = ['Bridge Loan Financing Bills May Not Meet Their May 8th Deadline Due to Lack\
 of Support.\
Sources report there will not be a vote regarding the authorization for the\
 bond issuance/bridge loan by the May 8th deadline.  Any possibility for a\
 deal has reportedly fallen apart.  According to sources, both the Republicans\
 and Democratic caucuses are turning against Davis.  The Democratic caucus\
 is reportedly "unwilling to fight" for Davis.  Many legislative Republicans\
 and Democrats reportedly do not trust Davis and express concern that, once\
 the bonds are issued to replenish the General Fund, Davis would "double\
 dip" into the fund.  Clearly there is a lack of good faith between the legislature\
 and the governor.  However, it is believed once Davis discloses the\
e details of the power contracts negotiated, a bond issuance will take place.\
  Additionally, some generator sources have reported that some of the long\
-term power contracts (as opposed to those still in development) require that\
hat the bond issuance happen by July 1, 2001.  If not, the state may be in \
breach of contract.  Sources state that if the legislature does not pass the\
 bridge loan legislation by May 8th, having a bond issuance by July 1st will\
 be very difficult.']
"""
"""
text = ['Bahah I can see your whole history \
Including the parts where you debated separating the chat you invited me to because I would make off with your technical papers \
Real nice']
"""
text_features = model.transform(text)
print (text_features.shape)
print (text_features)

#17.660 seconds to transform 8 examples
for i in range(len(text)):
	sentiment = text_features[i, 2388]
print(text[i],sentiment)