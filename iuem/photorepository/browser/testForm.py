from zope import interface
from zope import schema
from plone.autoform.form import AutoExtensibleForm
from z3c.form import form , button
from plone.z3cform import layout

class ITestForm(interface.Interface):
    """ItestForm"""
    vehicle = schema.Choice(title=u"Choice your vehicle",
                            description=u"for our next trip",
                            values=['Ferry boat','Car','Truck','motorcycle'])
    destination = schema.Choice(title=u"Where" ,
                                description=u"short or long trip",
                                values=['Brest','Brazil','Italia','Paris'])
    
class TestForm(AutoExtensibleForm , form.Form):
    schema = ITestForm
    ignoreContext = True
    
    method = "post"
            
    @button.buttonAndHandler(u"Ok, have a good trip")
    def goodTrip(self, action):
        data , errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        # changes = self.applyChanges(data)
        request = self.request
        print request.form
        print '-------'
        print data
        # nextUrl = '%s/@@test_view' % (self.context.absolute_url())
        # import pdb;pdb.set_trace()
        # request.response.redirect(nextUrl)
    
    def action(self):
        return self.context.absolute_url() + '/@@test_view'

class TestFormView(layout.FormWrapper):
    label = u"Choice your trip here"
    form = TestForm
    