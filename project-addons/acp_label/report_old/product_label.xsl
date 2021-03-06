<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:template match="etikettseite">
<document filename="etiquetasproductos.pdf">
<template pageSize="(50mm, 50mm)" 
         leftMargin="1.4mm" rightMargin="1.4mm" topMargin="0mm" bottomMargin="0mm" 
         title="Etikett" author="Generated by Open ERP">
<pageTemplate id="all">
   <frame id="first" x1="0" y1="0" width="50mm" height="50mm"/>
</pageTemplate>
</template>
<stylesheet>
<paraStyle name="st_pn"      fontName="Helvetica" leading="10" fontSize="10" spaceBefore="1mm" spaceAfter="0" alignment="center"/>

<paraStyle name="st_product" fontName="Helvetica" leading="7" fontSize="7"  spaceBefore="0"   spaceAfter="0"/>
<paraStyle name="st_product1" fontName="Helvetica" leading="7" fontSize="6"  spaceBefore="0"   spaceAfter="0"/>
<paraStyle name="st_product2" fontName="Helvetica-Bold" leading="7" fontSize="8"  spaceBefore="0"   spaceAfter="0"/>
<paraStyle name="st_product_name" height="30mm" fontName="Helvetica" leading="7" fontSize="7"  spaceBefore="0"   spaceAfter="0"/>
<paraStyle name="st_loc"     fontName="Helvetica" leading="0" fontSize="7"  spaceBefore="0"   spaceAfter="0" alignment="right"/>
<paraStyle name="st_slogan"  fontName="Helvetica" leading="0" fontSize="6"  spaceBefore="0"   spaceAfter="0" alignment="left"/>
</stylesheet>
<story>
<xsl:apply-templates select="produktetikett" mode="story"/>
</story>
</document>
</xsl:template>

<xsl:template match="produktetikett" mode="story">

        

  		<blockTable   rowHeights="5mm">
			<tr> 
				<td> <para style="st_product_name" ><xsl:value-of select="pname"/></para> </td> 
			</tr>
				
		</blockTable>        
  		<blockTable   rowHeights="3mm">
			<tr> 

				<td> <para style="st_product1" ><xsl:value-of select="precio_antes"/></para>   </td> 				

			</tr>
			<tr> 
				<td> <para style="st_product2" ><xsl:value-of select="precio"/></para>   </td> 								
			</tr>						
		</blockTable>
		          
                
              

        <barCode code="ean13" barWidth="1.0" barHeight="40">
            <xsl:value-of select="ean13"/>
        </barCode>

  		<blockTable   rowHeights="4mm">
			<tr> 
				<td> <para style="st_product" >Codigo: <xsl:value-of select="default_code"/></para> </td> 
			</tr>				
		</blockTable>         
  		<blockTable   rowHeights="4mm">
			<tr> 
				<td> <para style="st_product" >Marca: <xsl:value-of select="marca_id"/></para> </td> 
			</tr>				
		</blockTable> 
  		<blockTable   rowHeights="4mm">
			<tr> 
				<td> <para style="st_product" >Talla: <xsl:value-of select="talla"/></para> </td> 
			</tr>				
		</blockTable> 
  		<blockTable   rowHeights="4mm">
			<tr> 
				<td> <para style="st_product" >Color: <xsl:value-of select="color"/></para> </td> 
			</tr>				
		</blockTable> 
        
  
        <spacer length="1mm"/>
        <para style="st_slogan">
            GRUPO NOVA MARACANÁ, S.L.
        </para>


</xsl:template>

</xsl:stylesheet>
