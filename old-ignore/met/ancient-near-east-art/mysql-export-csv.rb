#!/bin/env ruby
# frozen_string_literal: true

require 'optparse'
require 'mysql2'
require 'csv'

options = {}

OptionParser.new do |opts|
  opts.banner = "Usage #{$PROGRAM_NAME} options"

  opts.on('-u', '--user MANDATORY', 'username for the database connection ') do |v|
    options[:user] = v
  end

  opts.on('-p', '--password MANDATORY', 'password for the database connection ') do |v|
    options[:password] = v
  end

  opts.on('-h', '--hostname MANDATORY', 'hostname for the database connection ') do |v|
    options[:hostname] = v
  end

  opts.on('-d', '--database MANDATORY', 'database where to execute the query ') do |v|
    options[:database] = v
  end

  opts.on('-q', '--query MANDATORY', 'query to execute') do |v|
    options[:query] = v
  end

  opts.on('-o', '--output MANDATORY', 'output file where to save the result') do |v|
    options[:output] = v
  end

  opts.on_tail('-h', '--help', 'show these options :-) ') do
    puts opts
    exit
  end
end.parse!

sqlClient = Mysql2::Client.new(host: options[:host], username: options[:user],
                               password: options[:password], database: options[:database])

rs = sqlClient.query(options[:query])

rowCount = 0
CSV.open(options[:output], 'wb') do |csv|
  rs.each do |row|
    if rowCount == 0
      header = row.keys
      csv << header
    end
    csvRow = []
    row.each do |_key, value|
      csvRow.push(value)
    end
    csv << csvRow
    rowCount += 1
  end
end

puts (rowCount + 1).to_s + ' records exported in ' + options[:output]
sqlClient.close
