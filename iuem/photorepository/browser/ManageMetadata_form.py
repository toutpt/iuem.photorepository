from five import grok
from plone.directives import form

from zope import schema
from z3c.form import button , field
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import adapts
from Products.ATContentTypes.interface import IATFolder
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from iuem.photorepository import iuemMessageFactory as _
from Products.AddRemoveWidget import AddRemoveWidget
from plone.z3cform import layout
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import INormalizer

class metadataSource(object):
    grok.implements(IContextSourceBinder)
    
    def __init__(self,k):
        self.k = k
        
    def __call__(self , context):
        normalizer = getUtility(INormalizer)
        w = []
        if self.k == 'description' or self.k == 'photographer' or self.k == 'recording_date_time':
            w.append(SimpleVocabulary.createTerm('description','description',context[self.k]))
            return SimpleVocabulary(w)
        for ww in context[self.k]:
            nww = normalizer.normalize(unicode(ww , 'utf-8'), locale = 'fr')
            uww = unicode(ww , 'utf-8')
            w.append(SimpleVocabulary.createTerm(nww,nww,uww))   
        return SimpleVocabulary(w)
    
class IManageMetadataForm(form.schema.Schema):
    """metadata form"""
    """
    ptype = schema.Choice(title=u"Type", description=u"File type",values=['test'])
    autor = schema.ASCIILine(title=u"Auteur",
                             description=u"a person")
    """
    whereToSpread  = schema.Choice(title=u"Where to spread",
                     required=True,
                     description=u"Only images = only images in this Folder; Everywhere = to all images and folders under this folder",
                     values=['Only Images','Everywhere']
                     )
    addOrReplace   = schema.Choice(title=_(u"Add or Replace"),
                     required=False,
                     description=_(u"Add = add metadatas to metadatas yet present; Preplace = replace metadatas with metadatas of this Folder"),
                     values=['add','replace'],
                     default='add'
                     )
    description   = schema.Set(title=_(u"General Description"),
                     required=False,
                     description=_(u"General Description"),
                     value_type=schema.Choice(source=metadataSource('description'))
                     )
    general = schema.Set(title=u"general",
                     required=False,
                     description=_(u"general"),
                     value_type=schema.Choice(source=metadataSource('general'))
                     )
    science = schema.Set(title=u"science",
                     required=False,
                     description=_(u"science"),
                     value_type=schema.Choice(source=metadataSource('science'))
                     )
    where          = schema.Set(title=_(u"Localisation"),
                     required=False,
                     description=_(u"Localisations"),
                     value_type=schema.Choice(source=metadataSource('where'))
                     )
    laboratory     = schema.Set(title=u"Laboratory",
                     required=False,
                     description=_(u"Laboratories"),
                     value_type=schema.Choice(source=metadataSource('laboratory'))
                     )
    reseachproject = schema.Set(title=u"reseachproject",
                     required=False,
                     description=_(u"reseachproject"),
                     value_type=schema.Choice(source=metadataSource('reseachproject'))
                     )
    licencetype = schema.Set(title=u"licencetype",
                     required=False,
                     description=_(u"licencetype"),
                     value_type=schema.Choice(source=metadataSource('licencetype'))
                     )
    
    recording_date_time = schema.Set(title=u"recording_date_time",
                     required=False,
                     description=_(u"recording_date_time"),
                     value_type=schema.Choice(source=metadataSource('recording_date_time'))
                     )
    
    photographer = schema.Set(title=u"photographer",
                     required=False,
                     description=_(u"photographer"),
                     value_type=schema.Choice(source=metadataSource('photographer'))
                     )



class ManageMetadataForm(form.form.SchemaForm):
    """The form"""
    grok.name('manage_metadata')
    grok.require('zope2.View')
    grok.context(IATFolder)
    
    schema = IManageMetadataForm
    ignoreContext = True
    
    label = _(u"attribute metadata to images and/or folders")
    description = _(u"Decide where to spread metadatas and which metadatas")
    fields = field.Fields(IManageMetadataForm)
    fields['description'].widgetFactory = CheckBoxFieldWidget
    fields['where'].widgetFactory = CheckBoxFieldWidget
    fields['laboratory'].widgetFactory = CheckBoxFieldWidget
    fields['reseachproject'].widgetFactory = CheckBoxFieldWidget
    fields['general'].widgetFactory = CheckBoxFieldWidget
    fields['science'].widgetFactory = CheckBoxFieldWidget
    fields['licencetype'].widgetFactory = CheckBoxFieldWidget
    fields['recording_date_time'].widgetFactory = CheckBoxFieldWidget
    fields['photographer'].widgetFactory = CheckBoxFieldWidget

    def getContent(self):
        context = self.context
        data = {}
        data['description'] = context.Description()
        data['where'] = context.where
        data['laboratory'] = context.laboratory
        data['reseachproject'] = context.reseachproject
        data['general'] = context.general
        data['science'] = context.science
        data['licencetype'] = context.licencetype
        data['recording_date_time'] = context.recording_date_time
        data['photographer'] = context.photographer
        return data
        
    @button.buttonAndHandler(_(u'Spread Metadatas'),accessKey=u"o")
    def handleOk(self, action):
        data, errors = self.extractData()
        print data
        # print '============================'
        # print errors
        if errors:
            self.status = self.formErrorsMessage
            return
        request = self.request
        nextUrl = '%s/@@metadata_confirm_pt'%self.context.absolute_url()
        request.response.redirect(nextUrl)
    
    @button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        request = self.request
        nextUrl = self.context.absolute_url()
        request.response.redirect(nextUrl)

        
ManageMetadataFormView = layout.wrap_form(ManageMetadataForm)    

