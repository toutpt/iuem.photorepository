
from zope.publisher.browser import BrowserView
from iuem.photorepository.extender import ImageImageRepositoryExtender

class repoImageView(BrowserView):
    """new view for image repository
    """
    
    def unretour(self):
        context = self.context
        # import pdb;pdb.set_trace()
        return "str(context.request) "

    def sourceImage(self):
        context = self.context
        tag = '<img src="' + context.absolute_url() + '/sourceImage" '
        tag += 'ALT="' + str(context.title) + '" '
        tag += 'title="' + str(context.title) + '" '
        tag += 'height="' + str(context.sourceImage.height) + '" '
        tag += 'width="' + str(context.sourceImage.width) + '" '
        tag += '/>'
        return tag
    
    def viewImage(self):
        return self.context.tag()
    
    def description(self):
        return str(self.context.Description())

    def general(self):
        return  eval(str(self.context.general))

    def science(self):
        return  eval(str(self.context.science))
    
    def where(self):
        return eval(str(self.context.where))
    
    def laboratory(self):
        return eval(str(self.context.laboratory))
    
    def reseachproject(self):
        return eval(str(self.context.reseachproject))
    
    def licencetype(self):
        return eval(str(self.context.licencetype))
    
    def recording_date_time(self):
        return str(self.context.recording_date_time)
    
    def photographer(self):
        return str(self.context.photographer)

    def sourceExif(self):
        try:
            return eval(str(self.context.exif))
        except:
            return False
            