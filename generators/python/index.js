var path = require('path');
var slugify = require('slugify');

var Generator = require('yeoman-generator');

module.exports = class extends Generator{
  constructor(args, opts) {
    super(args, opts);
    this.argument('function-name', {
      desc: 'Name of the function to generate',
      type: String,
      required: true
    });
  }

  initializing() {
    this.composeWith(require.resolve('../app'));
  }

  prompting() {
    var done = this.async();
    this.prompt([{
      type    : 'input',
      name    : 'description',
      message : 'Function Description:'
    }]).then(function(answers, err) {
      this.meta = {};
      this.meta.functionName = slugify(this.options['function-name'], '_');
      this.meta.description = answers.description;
      done(err);
    }.bind(this));
  }

  configuring() {
    // Copy all the normal files.
    this.fs.copy(
      this.templatePath("**/*"),
      this.destinationRoot()
    );
  }

  writing() {
    this.fs.copyTpl(
      this.templatePath('functions/lambda_tmpl/**'),
      this.destinationPath(path.join('functions', this.options['function-name'])),
      { meta: this.meta }
    );

    this.fs.delete(
      this.destinationPath(path.join('functions','lambda_tmpl'))
    );
  }

  install() {
    var currSubFolder = 'functions/' + this.options['function-name'];
    var currRequirements = currSubFolder + '/requirements.txt';
    this.spawnCommand('cd', [currSubFolder])
    this.spawnCommand('pip3', ['install', '-r', currRequirements, '-t', currSubFolder])
  }

  end() {
    this.log("Success! You may edit your new function in the 'functions/' folder\n")
  }
}
