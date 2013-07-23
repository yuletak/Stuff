#!/bin/env /opt/chef/embedded/bin/ruby

class TClass
    def initialize(att1=nil)
        @att1 = att1
        @att2 = 0
        @att3 = 3
    end
    attr_accessor :att1
    attr_accessor :att2
    attr_accessor :att3
end

obj = TClass.new(6)
puts obj.att1
puts obj.att2
puts obj.att3

TClass.instance_methods
