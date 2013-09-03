#!/bin/env /usr/bin/ruby

# paranthesis are used to return the following
# index:
#   0 - FQDN
#   1 - hostname
#   2 - hc host number
#   3 - cp host number
#   4 - ci host number
#   5 - domain
hName = /^(hc([1-9]|1[0-2])|cp(310[1-5])|ci(1))(\.\w+)*$/
while (1) do
    puts 'input value:'
    
    # chomp removes newline
    input = gets.chomp
    if input == 'quit'
        exit 
    end
    host = hName.match(input)
    if host
        puts 'hostname:  ' + host[1]
        for i in host[2..4] do
            if i != nil
                number = i
            end
        end
        if number
            puts 'hostnumber:  '+number
        end
    else 
        puts 'no match!'
    end
end
