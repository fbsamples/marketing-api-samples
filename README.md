** THIS REPO HAS BEEN ARCHIVED AND IS NO LONGER BEING ACTIVELY MAINTAINED **

# Facebook Marketing API Samples (Muse)
Facebook Marketing API Samples is a package of samples that demonstrate how to
use the Marketing API SDK to implement actual use cases.

## Requirements
- Python 2.7
- pip [install guide](https://pip.pypa.io/en/stable/installing/)
- PostgreSQL [install guide](https://wiki.postgresql.org/wiki/Detailed_installation_guides)

## Setting up Facebook Marketing API Samples
- Install virtualenv and virtualenvwrapper

			sudo pip install virtualenv
			sudo pip install virtualenvwrapper --ignore-installed

- Add these lines to `~/.bashrc` or `~/.bash_profile` depending on your system

			export WORKON_HOME=~/envs
			source /usr/local/bin/virtualenvwrapper.sh

- Close and reopen terminal. Make a new virtual environment called `muse`:

			mkvirtualenv muse -a /your/path/to/muse

- From now on you can switch to this environment by using the `workon` command:

			workon muse

- Install muse dependencies:

			pip install -r requirements.txt

- Update the setting file:

			workon muse
			vim $VIRTUAL_ENV/bin/postactivate

- Add this to `postactivate` file:

			export DJANGO_SETTINGS_MODULE="muse.settings"
			export FACEBOOK_APP_ID="app_id for an app that supports https://localhost:8000"
			export FACEBOOK_APP_SECRET="the app secret for the above app"

- Samples metadata is stored in and served from a database. To get sample metadata inserted into your local database run this command:

			python manage.py migrate

- Before you can run the site, the project uses [npm](https://www.npmjs.com/) and a [gulp](http://gulpjs.com/) process to build the JavaScript files for the UI components. The `package.json` script contains a `postinstall` task that does the building. To install and initialize this, make sure you have [Node.js](https://nodejs.org/en/) and npm installed, then run

			npm install

- Finally, run Muse site locally:

			python manage.py runsslserver

- Open your browser and go to `https://localhost:8000` to see the running site

## How Facebook Marketing API Samples works
Each sample is a self contained Python script located in muse/samples/samplecode. This script doesn't need to be concerned with user input validation, login, or displaying results. It only needs to be concerned with the solution it provides. The goal is that the marketing developer can copy this script and run it in their own environment using only python.

To let developers discover and play with samples, the functionality is exposed online using a Django view and associated form and template.

To display a gallery of samples and dispatch requests to the sample view, we also need some metadata about the sample including name, description, sample view name, and a unique string id that becomes the sample's URL on the site.

So each sample consists of:

1. Sample script containing the solution code that developers can use
2. Sample Django view, form and html template
3. Sample metadata

### Writing a New Sample Script
Create a new python module in `samples/samplecode`. Write your sample code using the Python Ads API SDK. Assume the SDK is already initialized with the user's access token so you don't need to worry about that.

Write one main class that is named with your sample name e.g. `AwesomeSolutionSample`. This class should have one method that is your sample's entry point. It can have any other methods or attributes that make sense but they are not to be called by external code. Be thoughtful in factoring your code into classes and methods to make more readable and reusable.

Use python docstrings at the module level to provide information that will be displayed at the top of your sample's web page. Start with a title then an overview of what the sample does. Include links to relevant developer docs.

Use Python docstrings at the class and method level to provide information that will be displayed at the bottom of your sample's web page as code documentation.

### Writing a New Sample View
Create a new python module in `samples/views`. In this module, write a Django class-based view and its associated form.

The view needs to support GET so that a user can view your sample page. Most samples will also have a form to collect user input, such as which ad account to use, so the view needs to also support POST.

In MUSE, we collected the common code required for each sample into common View and Form classes:

- SampleBaseView in `samples/views/sample.py`
- ComponentForm in `common/components/component_form.py`

The `ComponentForm` will implement form wide validations and other form level logic that should be shared across samples. The `SampleBaseView` will use the base sample template from `muse/samples/templates/samples/sample_form.html`. This templates will simply render the form object from your sample view, so you don't have to write your own template. If you need to customize you can:

- Define `BUTTON_TEXT` class variable at your sample view class to override the text appearing on the sample's run button. Or
- Define `TEMPLATE` class variable at your sample view class to change the default sample form template.
Checkout the Carousel App Ad sample as a reference.

## Add Sample Metadata
To show the sample in the list view, you need to add the sample metadata. Edit and add the following migration code into the file `dash/migrations/9999_auto_samples_metadata.py`:

		Sample.objects.create(
			view_class="<SAMPLE_VIEW_CLASS_NAME>",
			description="<SAMPLE_VIEW_DESCRIPTION>",
			view_module="<SAMPLE_VIEW_MODULE_NAME>",
			seo_description="<SAMPLE_VIEW_DESCRIPTION>",
			friendly_name="<SAMPLE_VIEW_FRIENDLY_NAME>",
			roles_to_check="",
			id="<URL_EXTENSION>")

After editing the migration file, run the migration:

		python manage.py migrate

Find the sample you just created in the sample list `https://127.0.0.1:8000/samples`.

## License
Please refer to the LICENSE file.
