import favorite
auth = favorite.pickleLoad()
if auth!= None:
	favorite.unfavorite(favorite.IDFile, auth)
