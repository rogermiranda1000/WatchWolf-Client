# MinecraftTester
A C++ library to test Minecraft Plugins

## Dependencies
- deps/[Botcraft](https://github.com/adepierre/Botcraft) (with [asio](https://think-async.com/Asio/Download.html) and [nlohmann json](https://github.com/nlohmann/json))
- Create a file `login.txt` with the following template: '&lt;Minecraft email&gt; &lt;Minecraft password&gt;\n'
- (Optional) `chmod 600 login.txt`

## Build
- create 'build' folder and enter inside it
- `cmake ..`
- `make`