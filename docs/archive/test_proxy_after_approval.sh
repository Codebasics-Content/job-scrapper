#!/bin/bash
# Test BrightData proxy after IP approval

echo "Testing proxy connection..."
curl -x http://brd-customer-hl_864cf5cf-zone-residential:gkl7gk6qk7s0@localhost:24000 https://lumtest.com/myip.json

echo -e "\n\nTesting JobSpy with proxy..."
python test_jobspy_linkedin.py
