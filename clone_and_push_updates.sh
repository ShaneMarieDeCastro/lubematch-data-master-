echo "SCRIPT TO PUSH TO TYPESENSE REPO"
git pull https://ACCESS_TOKEN_GITHUB@github.com/shellagilehub/nexus-typesense.git
git checkout githubactions
rm -rf data
cp /tmp/typesense .
git add .
git commit -m "Automation Rocks !!!"
git push https://ACCESS_TOKEN_GITHUB@github.com/shellagilehub/nexus-typesense.git