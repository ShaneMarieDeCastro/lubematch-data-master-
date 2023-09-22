echo "Deleting out folder"
rm -rf out
echo "Deleted out folder"
ses-cli products all en-AU --out cdn;
ses-cli products all en-CA --out cdn;
ses-cli products all fr-CA --out cdn;
ses-cli products all en-GB --out cdn;
ses-cli products all en-IN --out cdn;
ses-cli products all en-MY --out cdn;
ses-cli products all en-SG --out cdn;
ses-cli products all en-US --out cdn;
ses-cli products all zh-CN --out cdn;
ses-cli products all id-ID --out cdn;
ses-cli products all de-DE --out cdn;
ses-cli products all ru-RU --out cdn;
ses-cli products all en-PH --out cdn;
ses-cli products all en-IE --out cdn;
# ses-cli products all en-NZ --out cdn;

echo "Deleting xref.json"
rm -rf xref.json
echo "Deleted xref.json"
echo "Processing xref data"
ses-cli products xref > xref.json;
echo "Processed xref data"

echo "Deleting o2n.json"
rm -rf o2n.json
echo "Deleted o2n.json"
echo "Processing o2n data"
ses-cli products o2n > o2n.json;
echo "Processed o2n data"

echo "Deleting xref and o2n in typesense folder"
cd cli/typesense/;
rm -rf xref.json;
rm -rf o2n.json;
echo "Deleted xref and o2n in typesense folder"
echo "Copying xref and o2n in typesense folder"
cd ../..
cp xref.json cli/typesense/
cp o2n.json cli/typesense/

echo "Finished generating the data"