Here we provide the list of UI components we made for the [samples](/samples) so that you can easily re-use.

When we were developing the marketing automation samples we realized that there
are a lot of front tasks that are repeated across different samples, for example
populate the list of ad accounts of the logged in user, populate the list of the
custom audiences of the selected ad account, set the targeting specs for the ad
set etc. As a result, when we develop this sample site we decided to make those
UI components re-usable.

## How the Components Work
----

In a nut shell, a component is a customized [Django Form Field](https://docs.djangoproject.com/en/1.9/ref/forms/fields/).
The field is responsible of handling the data sent during the form submission and the widget used by the form takes care of the rendering of the field in the form.
In our components, we used JavaScript in addition to the default field to achieve the following:

- Add interaction and styling, for example the [selectize.js](http://selectize.github.io/selectize.js/) plugin at many select fields.
- Handles AJAX requests. We dynamically load data that are dependent on the value of other fields, such as custom audiences selector that is dependant on the selected ad account.
- Bootstrap [react](https://facebook.github.io/react/) components we built for more complex inputs such as the targeting spec.
{: class="test" }

At render time, we inject the initialization JavaScript code snippets for all components, like this:

~~~~{.language-javascript}
require(['components/components'], function(components) {
    components.initialize('components/actselect', 'id_act_select', 'previous_value');
});
~~~~

The module `components.js` has only one responsibility: encode/decode the previous value to render, require the corresponding JavaScript module and call the initialize function of that module.
The initialization function parameters always come in the following order:

- Module name
- Component element ID
- Previous value
- Extra parameters needed by the component, for example the account selector element ID that it listens to


##  How You Can Use Them
----
### In Django

If you are developing in Django environment, it's most straight forward, you can simple include the `components` folder that comes with the source code folder as an app in your Django project.
Then in your forms you should extend from the `ComponentForm` class. Then use the components like:

~~~~{.language-python}
from components.component_form import ComponentForm
from components.ad_account_select import AdAccountSelect

class MyForm(ComponentForm):
    ad_account = AdAccountSelect()
~~~~

Then the result of the field value will be available in the same name as you declared, similar to other native Django fields.

### In other frameworks

Not using Python or Django? You can still re-use the JavaScript code that handles the interaction, AJAX and react modals.
We currently use [requirejs](http://requirejs.org/) to dynamically load JavaScript modules, so make sure you get the dependencies for the components.
In order to get the same look and feel, you can use the [bootstrap](http://getbootstrap.com/) library. Some of our components assume that the HTML elements are structured in the bootstrap compatible way.

To use the `act_select.js` component, for example, you can do this in the HTML:

~~~~{.language-markup}
<div class="form-group">
    <label class="control-label" for="id_act_select">Ad Account</label>
    <div>
        <select class="form-control" id="id_act_select"></select>
        <script>
        require(['components/components'], function(components) {
            components.initialize('components/actselect', 'id_act_select', 'previous_value');
        });
        </script>
    </div>
</div>
~~~~
<br>
<div class="panel panel-default"><div class="panel-body">
<div class="form-group">
    <label class="control-label" for="id_act_select">Ad Account</label>
    <div>
        <select class="form-control" id="id_act_select"></select>
        <script>
        require(['components/components'], function(components) {
            components.initialize('components/actselect', 'id_act_select', 'previous_value');
        });
        </script>
    </div>
</div>
</div></div>
<br>

Notice we have a common contract for loading all the components:

~~~~{.language-javascript}
components.initialize(component_module_name, component_html_element_id, previous_value);
~~~~

The first param is the JavaScript module name, the second is the component's HTML element ID, the third is the previous value, and the additional parameters follow.

For the more complicated components that pops up a bootstrap modal window and outputs a JSON string value we need to do more work:

~~~~{.language-markup}
<div class="form-group">
    <label class="control-label" for="id_app_select">App</label>
    <div>
        <div class="input-group" id="id_app_select_container">
            <input class="form-control" readonly="readonly" icon="glyphicon glyphicon-plus" id="id_app_select" name="app" type="text" />
            <span class="input-group-addon" id="id_app_select_toggle" data-target="#id_app_select_modal">
                <i class="glyphicon glyphicon-plus">
                </i>
            </span>
        </div>
        <script>
        require(['components/components'], function(components) {
            components.initialize('components/app_select', 'id_app_select', '', 'id_act_select');
        });
        </script>
        <p class="help-block">Choose and ad account before using. Changing ad account will reset the selection.</p>
    </div>
</div>
~~~~

It renders something like this:

<br>
<div class="panel panel-default"><div class="panel-body">
<div class="form-group">
    <label class="control-label" for="id_app_select">App</label>
    <div>
        <div class="input-group" id="id_app_select_container">
            <input class="form-control" readonly="readonly" icon="glyphicon glyphicon-plus" id="id_app_select" name="app" type="text" />
            <span class="input-group-addon" id="id_app_select_toggle" data-target="#id_app_select_modal">
                <i class="glyphicon glyphicon-plus">
                </i>
            </span>
        </div>
        <script>
        require(['components/components'], function(components) {
            components.initialize('components/app_select', 'id_app_select', '', 'id_act_select');
        });
        </script>
        <p class="help-block">Choose and ad account before using. Changing ad account will reset the selection.</p>
    </div>
</div>
</div></div>
<br>

Notice that this component depends on the selected ad account so we are passing the element ID for the previous ad account selector `id_act_select`. The output for this type of component is a JSON formatted string.

### In React

If you are developing a web app using React, you can re-use the complex components because they are written in React, for example the `targeting_composer.jsx`. You can load this component into your React element by:

~~~~{.language-javascript}
React.render(
    new TargetingComposer({
        accountId: accountId,
        customAudiences: customAudiences,
        countryList: countryList,
        onChange: onChange,
        initialValue: initialSpec,
    }),
    document.getElementById(reactElementId)
);
~~~~

##  UI Components Gallery
----

Check the components in action at the [components gallery](/components/gallery) page.
