import { NextResponse } from "next/server";
import { PutObjectCommand, S3Client } from "@aws-sdk/client-s3";
export async function POST(request: Request) {
 const { prompt } = await request.json(); const id=`asset_${crypto.randomUUID()}`;
 const record={id,prompt,workflow:"image-generate-v1",provider:"Genblaze",created_at:new Date().toISOString(),provenance_version:"1.0"};
 if(process.env.GENBLAZE_WORKER_URL){
  const response=await fetch(`${process.env.GENBLAZE_WORKER_URL.replace(/\/$/,"")}/generate`,{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({prompt})});
  if(!response.ok){
   const detail=await response.json().catch(()=>null);
   return NextResponse.json({error:detail?.detail||"Generation worker unavailable"},{status:response.status});
  }
  return NextResponse.json({...await response.json(),mode:"live"});
 }
 if(process.env.B2_ENDPOINT&&process.env.B2_BUCKET&&process.env.B2_KEY_ID&&process.env.B2_APPLICATION_KEY){
  const s3=new S3Client({region:process.env.B2_REGION||"us-west-004",endpoint:process.env.B2_ENDPOINT,credentials:{accessKeyId:process.env.B2_KEY_ID,secretAccessKey:process.env.B2_APPLICATION_KEY}});
  await s3.send(new PutObjectCommand({Bucket:process.env.B2_BUCKET,Key:`provenance/${id}.json`,Body:JSON.stringify(record,null,2),ContentType:"application/json"}));
  return NextResponse.json({id,model:"Genblaze workflow",mode:"live"});
 }
 return NextResponse.json({id,model:"Genblaze workflow",mode:"demo"});
}
