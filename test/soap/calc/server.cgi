# monkey-patch the Etc module, because its sysconfdir() method sometimes returns nil...
require "etc"
module Etc
  class << self
    alias_method :orig_sysconfdir, :sysconfdir
    def sysconfdir
      orig_sysconfdir() || ''
    end
  end
end

require 'bundler/setup'
require 'soap/rpc/cgistub'

class CalcServer < SOAP::RPC::CGIStub
  def initialize(*arg)
    super

    require_relative 'calc'
    servant = CalcService
    add_servant(servant, 'http://tempuri.org/calcService')
  end
end

status = CalcServer.new('CalcServer', nil).start
