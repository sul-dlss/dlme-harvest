# frozen_string_literal: true

server 'dlme-harvest.stanford.edu', user: 'harvester', roles: %w[web db app]

Capistrano::OneTimeKey.generate_one_time_key!
