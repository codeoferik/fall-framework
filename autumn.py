import sys
import os
import datetime
import json

logo = """
    --------------------------------------------------------------------------
    |                                                                        |
    |                                                        .\^/.           |
    |                 _                                    . |`|/| .         |
    |      __ _ _   _| |_ _   _ _ __ ___  _ __             |\|\|'|/|         |
    |     / _` | | | | __| | | | '_ ` _ \| '_ \         .--'-\`|/-''--.      |
    |    | (_| | |_| | |_| |_| | | | | | | | | |         \`-._\|./.-'/       |
    |     \__,_|\__,_|\__|\__,_|_| |_| |_|_| |_|          >`-._|/.-'<        |
    |                                                    '~|/~~|~~\|~'       |
    |                                                          |             |
    |                                                                        |
    --------------------------------------------------------------------------
"""
logoCommented = """
//    --------------------------------------------------------------------------
//    |                                                                        |
//    |                                                        .\^/.           |
//    |                 _                                    . |`|/| .         |
//    |      __ _ _   _| |_ _   _ _ __ ___  _ __             |\|\|'|/|         |
//    |     / _` | | | | __| | | | '_ ` _ \| '_ \         .--'-\`|/-''--.      |
//    |    | (_| | |_| | |_| |_| | | | | | | | | |         \`-._\|./.-'/       |
//    |     \__,_|\__,_|\__|\__,_|_| |_| |_|_| |_|          >`-._|/.-'<        |
//    |                                                    '~|/~~|~~\|~'       |
//    |                                                          |             |
//    |                                                                        |
//    --------------------------------------------------------------------------
"""


def log(data: str, isOk: bool) -> None:
    if not '--mute' in sys.argv:
        print(f'[autumn][{datetime.datetime.now().strftime("%H:%M:%S")}][{"OK" if isOk else "WARN"}]', data)

def divider(caption: str) -> None:
    width = os.get_terminal_size().columns
    print(f'\n{caption} {"-" * (width - len(caption) - 1)}')

def table(data: list, horizontalDivider: str = '', verticalDivider: str = '', headDivider: str = '') -> str:
    width = os.get_terminal_size().columns
    output = ''
    for rowIndex, row in enumerate(data):
        if rowIndex < 2 and headDivider: output += '\n' + headDivider * width
        else: output += '\n' + horizontalDivider * width
        for cellIndex, cell in enumerate(row):
            if cellIndex > 0: output += verticalDivider + ' '
            output += str(cell) + ' ' * (((width - len(verticalDivider + ' ')) // len(data[0])) - len(verticalDivider + ' ') - len(str(cell)))
    return output

def commands() -> None:
    commands = [
        ['COMMAND', 'DESCRIPTION', 'SYNTAX'],
        ['commands', 'lists all available commands.', 'autumn commands'],
        ['scaffold', 'scaffolds the project structure.', 'autumn scaffold [--mute to mute]'],

        ['start:prod', 'starts the application in production mode (ctrl + c to stop)', 'autumn start:prod'],
        ['start:dev', 'starts the application in development mode (ctrl + c to stop)', 'autumn start:dev'],

        ['make:helper', 'creates and links a helper', 'autumn make:helper [name] [--mute to mute]'],
        ['make:middleware', 'creates and links a middleware', 'autumn make:middleware [name] [--mute to mute]'],
        ['make:model', 'creates and links a model', 'autumn make:model [name] [--mute to mute]'],
        ['make:route', 'creates and links a route', 'autumn make:route [name] [--mute to mute]'],
        ['make:validator', 'creates and links a validator', 'autumn make:validator [name] [--mute to mute]'],

        ['delete:helper', 'deletes and unlinks a helper', 'autumn delete:helper [name] [--mute to mute]'],
        ['delete:middleware', 'deletes and unlinks a middleware', 'autumn delete:middleware [name] [--mute to mute]'],
        ['delete:model', 'deletes and unlinks a model', 'autumn delete:model [name] [--mute to mute]'],
        ['delete:route', 'deletes and unlinks a route', 'autumn delete:route [name] [--mute to mute]'],
        ['delete:validator', 'deletes and unlinks a validator', 'autumn delete:validator [name] [--mute to mute]'],

        ['list:routes', 'lists all application routes', 'autumn list:routes'],
    ]      

    print(logo)
    print(table(commands, '-', '|', '='))

def scaffold() -> None:
    divider('creating folders')
    baseFolders = ['helper', 'middlewares', 'models', 'routes', 'static', 'validators', 'views']
    for baseFolder in baseFolders:
        if os.path.isdir(baseFolder): log(f'skipping [{baseFolder}] folder as it already exists', False)
        else:
            os.mkdir(baseFolder)
            log(f'[{baseFolder}] folder created', True)

    divider('creating bundler')
    bundleFolders = ['helper', 'middlewares', 'models', 'validators']
    for bundleFolder in bundleFolders:
        if os.path.isfile(f'./{bundleFolder}/index.js'): log(f'skipping [{bundleFolder}] bundler as it already exists', False)
        else:
            bundler = open(f'./{bundleFolder}/index.js', 'w')
            bundler.write(logoCommented + '\n// this bundler is automatically managed by autumn, type autumn:commands to list all available commands')
            bundler.close()
            log(f'[{bundleFolder}] bundler created', True)

    divider('creating route autoloader')
    if os.path.isfile('./routes/index.js'): log('skipping the route autoloader as it already exists', False)
    else:
        autoloader = open('./routes/index.js', 'w')
        autoloader.write(logoCommented + """\n// this autoloader is automatically managed by autumn, type autumn:commands to list all available commands
const express = require('express')
const router = express.Router()

module.exports = router""")
        autoloader.close()
        log(f'route autoloader created', True)

    divider('creating cleanLogger helper')
    if os.path.isfile('./helper/cleanLogger.js'): log('skipping the cleanLogger helper as it already exists', False)
    else: 
        cleanLogger = open('./helper/cleanLogger.js', 'w')
        cleanLogger.write("""module.exports = function (log, isOk) {
	const date = new Date()
	let hours = date.getHours()
	let minutes = date.getMinutes()
	let seconds = date.getSeconds()
	if (hours < 10) hours = `0${hours}`
	if (minutes < 10) minutes = `0${minutes}`
	if (seconds < 10) seconds = `0${seconds}`
	const state = isOk ? 'OK' : 'WARN'
	console.log(`[fall][${hours}:${minutes}:${seconds}][${state}] ${log}`)
}
        """)
        cleanLogger.close()
        helperBundler = open('./helper/index.js', 'a')
        helperBundler.write("\nmodule.exports.cleanLogger = require('./cleanLogger')")
        helperBundler.close()
        log('cleanLogger helper created', True)

    divider('creating config files')
    if os.path.isfile('./.env'): log('skipping .env as it already exists', False)
    else:
        env = open('./.env', 'w')
        env.write(f"""APP_ROOT={os.getcwd()}
PROT=http
HOST=0.0.0.0
PORT=5000
        """)
        log('.env created', True)

    if os.path.isfile('./.env.example'): log('skipping .env.example as it already exists', False)
    else:
        envExample = open('./.env.example', 'w')
        envExample.write("""APP_ROOT=[root path to this directory]
PROT=[http or https]
HOST=[0.0.0.0 for localhost or the domainname]
PORT=[the port the application runs on]        
        """)

    if os.path.isfile('./.gitignore'): log('skipping .gitignore as it already exists', False)
    else:
        gitignore = open('./.gitignore', 'w')
        gitignore.write("""/node_modules
.env
.todo
        """)
        log('.gitignore created', True)

    if os.path.isfile('./.prettierrc'): log('skipping .prettierrc as it already exists.', False)
    else:
        prettierrc = open('./.prettierrc', 'w')
        prettierrc.write("""{
	"printWidth": 80,
	"tabWidth": 2,
	"useTabs": true,
	"semi": false,
	"singleQuote": true,
	"quoteProps": "as-needed",
	"jsxSingleQuote": true,
	"trailingComma": "none",
	"bracketSpacing": true,
	"jsxBracketSameLine": false,
	"arrowParens": "always",
	"requirePragma": false,
	"insertPragma": false,
	"proseWrap": "preserve",
	"htmlWhitespaceSensitivity": "css",
	"vueIndentScriptAndStyle": true,
	"endOfLine": "crlf"
}
        """)
        prettierrc.close()
        log('.prettierrc created', True)
    if os.path.isfile('./.todo'): log('skipping .todo as it already exists.', False)
    else:
        todo = open('./.todo', 'w')
        todo.close()
        log('.todo created', True)
    
    if os.path.isfile('./app.js'): log('skipping app.js as it already exists', False)
    else:
        app = open('./app.js', 'w')
        app.write("""require('dotenv').config()
const express = require('express')

const helper = require('./helper')
const routes = require('./routes')

const app = express()

app.use('/static', express.static('./static'))
app.use(routes)

const prot = process.env.PROT
const host = process.env.HOST
const port = process.env.PORT
app.listen(port, host, () => {
	helper.cleanLogger(`application listening on [${prot}://${host}:${port}]`, true)
    helper.cleanLogger(`application is running in [${process.env.NODE_ENV}] mode`, true)
})
        """)
        log('app.js created', True)

    divider('creating package.json')
    if os.path.isfile('./package.json'): log('skipping package.json as it already exists.', False)
    else:
        os.system('npm init -y')
        package = open('./package.json')
        packageFromJson = json.load(package)
        packageFromJson['scripts'] = {'start:prod': 'cross-env NODE_ENV=production node app', 'start:dev': 'cross-env NODE_ENV=development nodemon app'}
        package.close()
        package = open('./package.json', 'w')
        json.dump(packageFromJson, package)
        package.close()
        log('package.json created', True)

    divider('installing dependencies')
    if os.path.isdir('./node_modules'): log('skipping dependencies as the node_modules folder already exists', False)
    else:
        os.system('npm install --save-dev nodemon cross-env')
        os.system('npm install --save express dotenv')
    
    divider('opening app.js with vscode')
    os.system('code app.js')

def makeHelper() -> None:
    if len(sys.argv) < 3: log('missing name of helper, use autumn make:helper [name] or type autumn commands to list all available commands', False)
    else:
        helperName = sys.argv[2].replace('.js', '')
        if os.path.isfile(f'./helper/{helperName}.js'): log(f'skipping [{helperName}] helper as it already exists', False)       
        else:  
            helperFile = open(f'./helper/{helperName}.js', 'w')
            helperFile.write("""module.exports = function() {}""")
            helperFile.close()
            helperBundler = open('./helper/index.js', 'a')
            helperBundler.write(f"\nmodule.exports.{helperName} = require('./{helperName}')")
            helperBundler.close()
            os.system(f'code ./helper/{helperName}.js')
            log(f'[{helperName}] helper created', True)

def makeMiddleware() -> None:
    if len(sys.argv) < 3: log('missing name of middleware, use autumn make:middleware [name] or type autumn commands to list all available commands', False)
    else:
        middlewareName = sys.argv[2].replace('.js', '')
        if os.path.isfile(f'./middlewares/{middlewareName}.js'): log(f'skipping [{middlewareName}] middleware as it already exists', False)       
        else:  
            middlewareFile = open(f'./middlewares/{middlewareName}.js', 'w')
            middlewareFile.write("""module.exports = function(req, res, next) {}""")
            middlewareFile.close()
            middlewareBundler = open('./middlewares/index.js', 'a')
            middlewareBundler.write(f"\nmodule.exports.{middlewareName} = require('./{middlewareName}')")
            middlewareBundler.close()
            os.system(f'code ./middlewares/{middlewareName}.js')
            log(f'[{middlewareName}] middleware created', True)

def makeModel() -> None:
    if len(sys.argv) < 3: log('missing name of model, use autumn make:model [name] or type autumn commands to list all available commands', False)
    else:
        modelName = sys.argv[2].replace('.js', '')
        if os.path.isfile(f'./models/{modelName}.js'): log(f'skipping [{modelName}] model as it already exists', False)       
        else:  
            modelFile = open(f'./models/{modelName}.js', 'w')
            modelFile.write("""module.exports = function() {}""")
            modelFile.close()
            modelBundler = open('./models/index.js', 'a')
            modelBundler.write(f"\nmodule.exports.{modelName} = require('./{modelName}')")
            modelBundler.close()
            os.system(f'code ./models/{modelName}.js')
            log(f'[{modelName}] model created', True)

def makeRoute() -> None:
    if len(sys.argv) < 3: log('missing name of route, use autumn make:route [name] or type autumn commands to list all available commands', False)
    else:
        routeName = sys.argv[2].replace('.js', '')
        if os.path.isfile(f'./routes/{routeName}.js'): log(f'skipping [{routeName}] route as it already exists', False)       
        else:  
            routeFile = open(f'./routes/{routeName}.js', 'w')
            routeFile.write("""const express = require('express')

const router = express.Router()

module.exports = router""")
            routeFile.close()
            routeAutoloader = open('./routes/index.js')
            routeAutoloaderLines = routeAutoloader.readlines()
            routeAutoloader.close()
            routeAutoloader = open('./routes/index.js', 'w')
            for routeAutoloaderLine in routeAutoloaderLines[:-1]:
                routeAutoloader.write(routeAutoloaderLine)
            routeAutoloader.write(f"router.use(require('./{routeName}'))\n")
            routeAutoloader.write(routeAutoloaderLines[-1])
            routeAutoloader.close()
            os.system(f'code ./routes/{routeName}.js')
            log(f'[{routeName}] route created', True)

def makeValidator() -> None:
    if len(sys.argv) < 3: log('missing name of validator, use autumn make:validator [name] or type autumn commands to list all available commands', False)
    else:
        validatorName = sys.argv[2].replace('.js', '')
        if os.path.isfile(f'./validators/{validatorName}.js'): log(f'skipping [{validatorName}] validator as it already exists', False)       
        else:  
            modelFile = open(f'./validators/{validatorName}.js', 'w')
            modelFile.write("""module.exports = function() {}""")
            modelFile.close()
            modelBundler = open('./validators/index.js', 'a')
            modelBundler.write(f"\nmodule.exports.{validatorName} = require('./{validatorName}')")
            modelBundler.close()
            os.system(f'code ./validators/{validatorName}.js')
            log(f'[{validatorName}] validator created', True)

def deleteHelper() -> None:
    if len(sys.argv) < 3: log('missing name of helper, use autumn delete:helper [name] or type autumn commands to list all available commands', False)
    else:
        helperName = sys.argv[2].replace('.js', '')
        if not os.path.isfile(f'./helper/{helperName}.js'): log(f'skipping [{helperName}] helper as it does not exist', False)
        else:
            os.remove(f'./helper/{helperName}.js')
            helperBundler = open('./helper/index.js', 'r')
            helperBundlerLines = helperBundler.readlines()
            helperBundler.close()
            helperBundler = open('./helper/index.js', 'w')
            helperBundlerLines = [helperBundlerLine for helperBundlerLine in helperBundlerLines if f"module.exports.{helperName} = require('./{helperName}')" not in helperBundlerLine]
            for helperBundlerLine in helperBundlerLines:
                helperBundler.write(helperBundlerLine)
            helperBundler.close()
            log(f'[{helperName}] helper deleted', True)

def deleteMiddleware() -> None:
    if len(sys.argv) < 3: log('missing name of middleware, use autumn delete:middleware [name] or type autumn commands to list all available commands', False)
    else:
        middlewareName = sys.argv[2].replace('.js', '')
        if not os.path.isfile(f'./middlewares/{middlewareName}.js'): log(f'skipping [{middlewareName}] middlewares as it does not exist', False)
        else:
            os.remove(f'./middlewares/{middlewareName}.js')
            middlewareBundler = open('./middlewares/index.js', 'r')
            middlewareBundlerLines = middlewareBundler.readlines()
            middlewareBundler.close()
            middlewareBundler = open('./middlewares/index.js', 'w')
            middlewareBundlerLines = [middlewareBundlerLine for middlewareBundlerLine in middlewareBundlerLines if f"module.exports.{middlewareName} = require('./{middlewareName}')" not in middlewareBundlerLine]
            for middlewareBundlerLine in middlewareBundlerLines:
                middlewareBundler.write(middlewareBundlerLine)
            middlewareBundler.close()
            log(f'[{middlewareName}] middlewares deleted', True)

def deleteModel() -> None:
    if len(sys.argv) < 3: log('missing name of model, use autumn delete:model [name] or type autumn commands to list all available commands', False)
    else:
        modelName = sys.argv[2].replace('.js', '')
        if not os.path.isfile(f'./models/{modelName}.js'): log(f'skipping [{modelName}] models as it does not exist', False)
        else:
            os.remove(f'./models/{modelName}.js')
            modelBundler = open('./models/index.js', 'r')
            modelBundlerLines = modelBundler.readlines()
            modelBundler.close()
            modelBundler = open('./models/index.js', 'w')
            modelBundlerLines = [modelBundlerLine for modelBundlerLine in modelBundlerLines if f"module.exports.{modelName} = require('./{modelName}')" not in modelBundlerLine]
            for modelBundlerLine in modelBundlerLines:
                modelBundler.write(modelBundlerLine)
            modelBundler.close()
            log(f'[{modelName}] models deleted', True)

def deleteRoute() -> None:
    if len(sys.argv) < 3: log('missing name of route, use autumn delete:route [name] or type autumn commands to list all available commands', False)
    else:
        routeName = sys.argv[2].replace('.js', '')
        if not os.path.isfile(f'./routes/{routeName}.js'): log(f'skipping [{routeName}] routes as it does not exist', False)
        else:
            os.remove(f'./routes/{routeName}.js')
            routeBundler = open('./routes/index.js', 'r')
            routeBundlerLines = routeBundler.readlines()
            routeBundler.close()
            routeBundler = open('./routes/index.js', 'w')
            routeBundlerLines = [routeBundlerLine for routeBundlerLine in routeBundlerLines if f"router.use(require('./{routeName}'))" not in routeBundlerLine]
            for routeBundlerLine in routeBundlerLines:
                routeBundler.write(routeBundlerLine)
            routeBundler.close()
            log(f'[{routeName}] routes deleted', True)

def deleteValidator() -> None:
    print('test')
    if len(sys.argv) < 3: log('missing name of validator, use autumn delete:validator [name] or type autumn commands to list all available commands', False)
    else:
        validatorName = sys.argv[2].replace('.js', '')
        if not os.path.isfile(f'./validators/{validatorName}.js'): log(f'skipping [{validatorName}] validators as it does not exist', False)
        else:
            os.remove(f'./validators/{validatorName}.js')
            validatorBundler = open('./validators/index.js', 'r')
            validatorBundlerLines = validatorBundler.readlines()
            validatorBundler.close()
            validatorBundler = open('./validators/index.js', 'w')
            validatorBundlerLines = [validatorBundlerLine for validatorBundlerLine in validatorBundlerLines if f"module.exports.{validatorName} = require('./{validatorName}')" not in validatorBundlerLine]
            for validatorBundlerLine in validatorBundlerLines:
                validatorBundler.write(validatorBundlerLine)
            validatorBundler.close()
            log(f'[{validatorName}] validators deleted', True)

def listRoutes() -> None:
    routes = [['METHOD', 'PATH', 'MIDDLEWARES']]
    routeStrings = []
    for routeFileName in os.listdir('./routes'):
        if not routeFileName == 'index.js':
            routeFile = open(f'./routes/{routeFileName}', 'r')
            lines = routeFile.readlines()
            for lineIndex, line in enumerate(lines):
                wholeLine = ''
                if 'router.' in line:
                    wholeLine += line
                    if not '(req, res)' in line:
                        found = False
                        for subline in lines[lineIndex + 1:]:
                            if not found: wholeLine += subline
                            if '(req, res)' in subline:
                                found = True
                if wholeLine: routeStrings.append(wholeLine.replace('\n', '').replace('\t', '').strip())
    for routeString in routeStrings:
        route = []
        route.append(routeString.split('.')[1].split('(')[0].upper())
        route.append(routeString.split("'")[1])
        route.append(', '.join(routeString.split(",")[1:-2]))
        routes.append(route)
    print(table(routes, '-', '|', '='))

try:
    if sys.argv[1] == 'commands': commands()
    elif sys.argv[1] == 'scaffold': scaffold()

    elif sys.argv[1] == 'start:prod': os.system('npm run start:prod')
    elif sys.argv[1] == 'start:dev': os.system('npm run start:dev')

    elif sys.argv[1] == 'make:helper': makeHelper()
    elif sys.argv[1] == 'make:middleware': makeMiddleware()
    elif sys.argv[1] == 'make:model': makeModel()
    elif sys.argv[1] == 'make:route': makeRoute()
    elif sys.argv[1] == 'make:validator': makeValidator()

    elif sys.argv[1] == 'delete:helper': deleteHelper()
    elif sys.argv[1] == 'delete:middleware': deleteMiddleware()
    elif sys.argv[1] == 'delete:model': deleteModel()
    elif sys.argv[1] == 'delete:route': deleteRoute()
    elif sys.argv[1] == 'delete:validator': deleteValidator()

    elif sys.argv[1] == 'list:routes': listRoutes()
    else: log('invalid parameter, type autumn commands to list all available commands', False)
except IndexError:
    log('missing parameters, type autumn commands to list all available commands', False)