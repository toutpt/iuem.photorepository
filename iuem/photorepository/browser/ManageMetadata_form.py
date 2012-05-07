from five import grok
from plone.directives import form

from zope import schema
from z3c.form import button
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import adapts
from Products.ATContentTypes.interface import IATFolder
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from iuem.photorepository import iuemMessageFactory as _
from plone.autoform.form import AutoExtensibleForm
from plone.z3cform import layout
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import INormalizer

@grok.provider(IContextSourceBinder)
def possibleWhere(context):
    w = []
    # import pdb;pdb.set_trace()
    
    for ww in context['where']:
        normalizer = getUtility(INormalizer)
        nww = normalizer.normalize(unicode(ww , 'utf-8'), locale = 'fr')
        uww = unicode(ww , 'utf-8')
        w.append(SimpleVocabulary.createTerm(nww,nww,uww))   
    return SimpleVocabulary(w)

class metadataSource(object):
    grok.implements(IContextSourceBinder)
    def __init__(self,k):
        self.k = k
    def __call__(self , context):
        w = []
        for ww in context[self.k]:
            normalizer = getUtility(INormalizer)
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
    whereToSpread = schema.Choice(title=u"Where to spread",
                                  description=u"Description where to spread",
                                  values=['only Images','everywhere'])
    where = schema.Set(title=u"Localisation",
                                  description=_(u"Localisations"),
                                  value_type=schema.Choice(source=possibleWhere)
                                  )
    laboratory =schema.Set(title=u"Laboratory",
                                  description=_(u"Localisations"),
                                  value_type=schema.Choice(source=metadataSource('laboratory'))
                                  )

class ManageMetadataForm(form.form.SchemaForm):
    """The form"""
    grok.name('manage_metadata')
    grok.require('zope2.View')
    grok.context(IATFolder)
    
    schema = IManageMetadataForm
    ignoreContext = True
    
    label = u"distribute metadata values among objects"
    description = u"Decide where to spread metadatas"
    
    # import pdb;pdb.set_trace()

    def getContent(self):
        context = self.context
        # import pdb;pdb.set_trace()
        x = 'retour de getContent()'
        data = {}
        # import pdb;pdb.set_trace()
        data['where'] = context.where
        data['laboratory'] = context.laboratory
        
        return data
    
    @button.buttonAndHandler(u'Ok')
    def handleOk(self, action):
        data, errors = self.extractData()
        
        if errors:
            self.status = self.formErrorsMessage
            return
    
        
        
ManageMetadataFormView = layout.wrap_form(ManageMetadataForm)    
