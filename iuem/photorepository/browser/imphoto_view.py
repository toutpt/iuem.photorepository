from Products.Five import BrowserView
from zope.annotation.interfaces import IAnnotations
from iuem.photorepository.metadatamanager import METADATA_KEY


class imPhotoView(BrowserView):
    """a view"""
    
    def original(self):
        return 'Original photo'