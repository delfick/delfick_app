Delfick App
===========

An opinionated class to build a mainline executable.

Usage
-----

.. code-block:: python

    from my_app import MyApp, VERSION

    from delfick_app import App
    import logging

    class MyApp(App):

        # Setting both VERSION and boto_useragent_name
        # Will change boto's useragent to include {name}/{VERSION}
        # Not setting them means boto's useragent is unchanged
        VERSION = VERSION
        boto_useragent_name = "myapp"

        # Cli options for configuration special cli options
        cli_categories = ['app']
        cli_description = "My amazing app"
        cli_environment_defaults = {"CONFIG_LOCATION": ("--config", './config.yml')}
        cli_positional_replacements = [('--task', 'list_tasks'), '--environment']

        def execute(self, args, cli_args, logging_handler):
            app = MyApp()
            app.start(cli_args)

        def setup_other_logging(self, args, verbose=False, silent=False, debug=False):
            logging.getLogger("boto").setLevel([logging.CRITICAL, logging.ERROR][verbose or debug])

        def specify_other_args(self, parser, defaults):
            parser.add_argument("--task"
                , help = "The task to execute"
                , **defaults['--task']
                )

            parser.add_argument("--environment"
                , help = "the environment to use"
                , **defaults["--environment"]
                )

            parser.add_argument("--config"
                , help = "The configuration to use"
                , **defaults["--config"]
                )

    main = MyApp.main
    if __name__ == '__main__':
        main()

With the above configuration, the following three usages are equivalent::

    $ ./app.py some_task dev --config ./config.yml

    $ ./app.py --task some_task --environment dev --config ./config.yml

    $ APP_CONFIG=./config.yml ./app.py some_task dev

Installation
------------

Just use pip::

    $ pip install delfick_app

Tests
-----

Run the following::

    $ mkvirtualenv delfick_app
    $ workon delfick_app
    $ pip install -e .
    $ pip install -e ".[tests]"

To install delfick_app and it's dependencies.

Then to run the tests::

    $ ./test.sh

