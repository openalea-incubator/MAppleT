rm(list = ls())
plot_stress = function(titre,don,x,sphc,sphc_str,colors,charge,charge_str,type,pos_legend,lab_abs="masse sèche (g)"){
	print(titre)
	don = don[don$date >= "1998-05-16" & don$date <= "1998-10-15",]
	plot(don[don$sphc == sphc[1] & don$charge == charge[1],x] ~ date,data = don[don$sphc == sphc[1] & don$charge == charge[1],],col=colors[1],type="l",lty=type[1],lwd=2,
		main = titre,ylab = lab_abs,
		ylim = c(0,max(don[don$sphc %in% sphc & don$charge %in% charge,x]))
		)
	for(stress in 2:length(sphc)){
		lines(don[don$sphc == sphc[stress] & don$charge == charge[1],x] ~ date,data=don[don$sphc == sphc[stress] & don$charge == charge[1],],col=colors[stress],type="l",lty=type[stress],lwd=2)
		}
	legend(pos_legend,
			sphc_str,
			col = colors,
			lty = type,
			lwd = c(2,2,2,2),
			box.lty = 0,
			cex = 0.8,
			bg = NA
		)
}

plot_charge = function(titre,don,x,sphc,sphc_str,charge,charge_str,pos_legend,y_label){
	print(titre)
	don = don[don$date >= "1998-05-16" & don$date <= "1998-10-15",]

	colors_c = c("aquamarine3","chartreuse3","chocolate2","firebrick2")
	type_c = c(1,1,1,1)
	
	plot(don[don$sphc == sphc[1] & don$charge == charge[1],x] ~ don[don$sphc == sphc[1] & don$charge == charge[1],"date"],col=colors_c[1],type="l",lty=type_c[1],lwd=2,
		main = titre,
		ylim = c(0,max(don[don$sphc == sphc[1],x])),
		xlab = "date",
		ylab = y_label
		)

	for(ch in 2:length(charge)){
		lines(don[don$sphc == sphc[1] & don$charge == charge[ch],x] ~ date,data=don[don$charge == charge[ch] & don$sphc == sphc[1],],col=colors_c[ch],type="l",lty=type_c[ch],lwd=2)
		}
	legend(pos_legend,
			charge_str,
			col = colors_c,
			lty = type_c,
			lwd = c(2,2,2,2,2,2,2),
			box.lty = 0,
			title = "Taux de nouaison",
		)
}




sphc = c('_sphc103','_sphc104','_sphc105')
sphc_str = c("Non stressé","Stress modéré","Stress sévère")
colors = c("black","green","orange","red")
charge = c('_charge_10','_charge_30','_charge_50','_charge_75')
charge_str = c('10%','30%','50%','75%')

type = c(1,2,3,1,2,3)

somme = function(L){
	if(is.numeric(L)){
		return(sum(L,na.rm = T))
	}else
		return(L[1])
}

######### Graph avec croissance de tous les organes empillée ###############################################

croissance_tous_organes = function(don,sphc,charge){
	don = don[don$date >= "1998-05-16" & don$date <= "1998-10-15",]
	don = don[don$sphc == sphc & don$charge == charge,]
	don = don[order(don$date),]

	don$vb_s = don$vb_masse_seche
	don$vb_r = don$vb_s + don$vb_reserve_ms
	don$vr_s = don$vb_r + don$vr_masse_seche
	don$vr_r = don$vr_s + don$vr_reserve_ms

	don$tl_s = don$vr_r + don$tl_masse_seche
	don$tl_r = don$tl_s + don$tl_reserve_ms

	don$jr_s = don$tl_r + don$jr_masse_seche
	don$jr_r = don$jr_s + don$jr_reserve_ms

	don$pf_s = don$jr_r + don$pf_masse_seche
	don$pf_r = don$pf_s + don$pf_reserve_ms
	don$f2_s = don$pf_r + don$f2_masse_seche
	don$f2_r = don$f2_s + don$f2_reserve_ms	

	colors_o = c("#DB0000","#7F0000","#00A50B","#006B0A","#6D6D6D","#4C4C4C","#998509","#706006","#56210E","#38170A","#2D2D2D","#191919")

	plot(f2_r~date, data=don,type = "n",ylim=c(0,max(don$f2_r)), ylab="Masse sèche (g)")
	polygon(c(don$f2_r,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[1],border=NA)
	polygon(c(don$f2_s,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[2],border=NA)
	polygon(c(don$pf_r,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[3],border=NA)
	polygon(c(don$pf_s,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[4],border=NA)
	polygon(c(don$jr_r,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[7],border=NA)
	polygon(c(don$jr_s,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[8],border=NA)

	polygon(c(don$tl_r,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[5],border=NA)
	polygon(c(don$tl_s,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[6],border=NA)

	polygon(c(don$vr_r,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[9],border=NA)
	polygon(c(don$vr_s,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[10],border=NA)
	polygon(c(don$vb_r,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[11],border=NA)
	polygon(c(don$vb_s,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[12],border=NA)

	legend("topleft",
		c("Masse sêche de réserve des fruits","Masse sêche structurale des fruits",
		"m.s. de réserve des pousses feuillées","m.s. structurale des pousses feuillées",
		"m.s. de réserve du bois de un an","m.s. structurale du bois de un an",
		"m.s. de réserve des jeunes racines","m.s. structurale des jeunes racines",
		"m.s. de réserve des vielles racines","m.s. structurale des vielles racines",
		"m.s. de réserve du vieux bois","m.s. structurale du vieux bois"
		),
		fill = colors_o,
		border = NA,
		cex = 0.7,
		bty = "n"
	)

}

######## Besoins de croissance et respiration #################
 besoins_tous_organes = function(don,sphc,charge){	
	don = don[don$sphc == sphc & don$charge == charge,]
	don = don[order(don$date),]
	don = don[don$date>="1998-05-16" & don$date<="1998-10-15",]
	don$vb_s = don$vb_besoin_c_croiss
	don$vb_r = don$vb_s + don$vb_besoin_c_respi
	don$vr_s = don$vb_r + don$vr_besoin_c_croiss
	don$vr_r = don$vr_s + don$vr_besoin_c_respi

	don$tl_s = don$vr_r + don$tl_besoin_c_croiss
	don$tl_r = don$tl_s + don$tl_besoin_c_respi

	don$jr_s = don$tl_r + don$jr_besoin_c_croiss
	don$jr_r = don$jr_s + don$jr_besoin_c_respi

	don$pf_s = don$jr_r + don$pf_besoin_c_croiss
	don$pf_r = don$pf_s + don$pf_besoin_c_respi
	don$f2_s = don$pf_r + don$f2_besoin_c_croiss
	don$f2_r = don$f2_s + don$f2_besoin_c_respi	

	colors_o = c("#FF0000","#7F0000","#00E100","#007800","#ADADAD","#4C4C4C","#FFD800","#706006","#AF421D","#38170A","#75C5FF","#416E8E")

	plot(f2_r~date, data=don,type = "l",ylim=c(0,max(don$f2_r)), ylab = "demande de carbone ou phototsynthèse (g de carbone / jour)",lwd = 3,col="grey")
	lines(phot~date, data=don,type = "l",ylim=c(0,max(don$f2_r)),lwd = 3,lty=1)
	legend("bottomleft",
		c("Demande de carbone","Photosynthèse"),
		lty = c(1,1),
		col = c("grey","black"),
		border = NA,
		cex = 1,
		bty = "n",
		lwd = c(3,3)
	 )


	# plot(f2_r~date, data=don,type = "n",ylim=c(0,max(don$f2_r)), ylab = "Demande de croissance et de respiration (g de carbone)")
	# polygon(c(don$f2_r,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[1],border=NA)
	# polygon(c(don$f2_s,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[2],border=NA)
	# polygon(c(don$pf_r,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[3],border=NA)
	# polygon(c(don$pf_s,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[4],border=NA)
	# polygon(c(don$jr_r,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[7],border=NA)
	# polygon(c(don$jr_s,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[8],border=NA)

	# polygon(c(don$tl_r,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[5],border=NA)
	# polygon(c(don$tl_s,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[6],border=NA)

	# polygon(c(don$vr_r,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[9],border=NA)
	# polygon(c(don$vr_s,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[10],border=NA)
	# polygon(c(don$vb_r,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[11],border=NA)
	# polygon(c(don$vb_s,0,0)~c(don$date,max(don$date),min(don$date)),col=colors_o[12],border=NA)

	# lines(phot ~ date,data=don,type="l",lwd = 3,col="orange")

	# legend("topleft",
		# c("Demande de respiration des fruits","Demande de croissance des fruits",
		# "Demande de respiration des pousses feuillées","Demande de croissance des pousses feuillées",
		# "Demande de respiration du bois de un an","Demande de croissance du bois de un an",
		# "Demande de respiration des jeunes racines","Demande de croissance des jeunes racines",
		# "Demande de respiration des vielles racines","Demande de croissance des vielles racines",
		# "Demande de respiration du vieux bois","Demande de croissance du vieux bois"
		# ),
		# fill = colors_o,
		# border = NA,
		# cex = 0.7,
		# bty = "n"
	# )
}

svg("demande.svg")
besoins_tous_organes(data,'_sphc103',"")
dev.off()


####################################################################################

appercu = function(data,pdffile){
	pdf(file = pdffile)
	croissance_tous_organes(data,'_sphc103',"")
	besoins_tous_organes(data,'_sphc103',"")

	plot_stress("m.s. des pousses feuillées en fonction du stress hydrique",data,"pf_masse_seche",sphc,sphc_str,colors,'',charge_str,type,"bottomright")
	plot_stress("m.s. des fruits en fonction du stress hydrique",data,"f2_masse_seche",sphc,sphc_str,colors,'',charge_str,type,"bottomright")
	plot_stress("m.s. du bois de 1 an en fonction du stress hydrique",data,"tl_masse_seche",sphc,sphc_str,colors,'',charge_str,type,"bottomright")
	plot_stress("m.s. du vieux bois en fonction du stress hydrique",data,"vb_masse_seche",sphc,sphc_str,colors,'',charge_str,type,"bottomright")
	plot_stress("m.s. des jeunes racines en fonction du stress hydrique",data,"jr_masse_seche",sphc,sphc_str,colors,'',charge_str,type,"bottomright")
	plot_stress("m.s. des vielles racines en fonction du stress hydrique",data,"vr_masse_seche",sphc,sphc_str,colors,'',charge_str,type,"bottomright")

	plot_stress("Assimilation de carbone (gc.day-1)",data,"phot",sphc,sphc_str,colors,charge,charge_str,type,"bottomright")

	plot_stress("Masse sèche de réserves des pousses feuillées (fraction du total)",data,"pf_reserve_ms_p",sphc,sphc_str,colors,charge,charge_str,type,"bottomright")
	plot_stress("Masse sèche de réserves du bois de 1 an (fraction du total)",data,"tl_reserve_ms_p",sphc,sphc_str,colors,charge,charge_str,type,"bottomright")
	plot_stress("Masse sèche de réserves du vieux bois (fraction du total)",data,"vb_reserve_ms_p",sphc,sphc_str,colors,charge,charge_str,type,"bottomright")
	plot_stress("Masse sèche de réserves du vielles racines (fraction du total)",data,"vr_reserve_ms_p",sphc,sphc_str,colors,charge,charge_str,type,"bottomright")
	plot_stress("Masse sèche de réserves des jeunes racines (fraction du total)",data,"jr_reserve_ms_p",sphc,sphc_str,colors,charge,charge_str,type,"bottomright")


	plot_stress("Besoin de croissance des fruits (fraction du total)",data,"f2_besoin_c_croiss",sphc,sphc_str,colors,charge,charge_str,type,"bottomright")

	plot_charge("m.s. des pousses feuillées en fonction de la charge (Irrigation a satiete)",data,"pf_masse_seche",'_sphc103',sphc_str,charge,charge_str,"bottomright")
	plot_charge("m.s. des fruits en fonction de la charge (Irrigation a satiete)",data,"f2_masse_seche",'_sphc103',sphc_str,charge,charge_str,"bottomright")
	plot_charge("m.s. moyenne des fruits en fonction de la charge (Irrigation a satiete)",data,"f2_ms_moy",'_sphc103',sphc_str,charge,charge_str,"bottomright")
	plot_charge("m.s. du bois de 1 an en fonction de la charge (Irrigation a satiete)",data,"tl_masse_seche",'_sphc103',sphc_str,charge,charge_str,"bottomright")
	plot_charge("m.s. du vieux bois en fonction de la charge (Irrigation a satiete)",data,"vb_masse_seche",'_sphc103',sphc_str,charge,charge_str,"bottomright")
	plot_charge("m.s. des jeunes racines en fonction de la charge (Irrigation a satiete)",data,"jr_masse_seche",'_sphc103',sphc_str,charge,charge_str,"bottomright")
	plot_charge("m.s. des vielles racines en fonction de la charge (Irrigation a satiete)",data,"vr_masse_seche",'_sphc103',sphc_str,charge,charge_str,"bottomright")

	plot_charge("Assimilation de carbone (gc.day-1)",data,"phot",'_sphc103',sphc_str,charge,charge_str,"bottomright")

	plot_charge("Masse sèche de réserves des pousses feuillées (fraction du total)",data,"pf_reserve_ms_p",'_sphc103',sphc_str,charge,charge_str,"bottomright")
	plot_charge("Masse sèche de réserves du bois de 1 an",data,"tl_reserve_c",'_sphc103',sphc_str,charge,charge_str,"bottomright")
	plot_charge("Masse sèche de réserves du vieux bois",data,"vb_reserve_c",'_sphc103',sphc_str,charge,charge_str,"bottomright")

	plot_charge("Besoins de croissance des fruits",data,"f2_besoin_c_croiss",'_sphc103',sphc_str,charge,charge_str,"bottomright")

	plot_stress("Ratio offre/demande",data,"ratio_offre_demande",sphc,sphc_str,colors,charge,charge_str,type,"bottomright")
	plot_charge("Ratio offre/demande",data,"ratio_offre_demande",'_sphc103',sphc_str,charge,charge_str,"bottomright")
	plot_stress("Demande totale (croissance + respiration)",data,"demande_tot",sphc,sphc_str,colors,charge,charge_str,type,"bottomright")
	plot_charge("Demande totale (croissance + respiration)",data,"demande_tot",'_sphc103',sphc_str,charge,charge_str,"bottomright")



	dev.off()
}


##### Simulations fuji_0 à fuji_3 #####


inutiles = c("gd_surface_foliaire","gd_nombre_unites","gd_taux_phot_max","gd_masse_seche","gd_reserve_c","gd_besoin_c_croiss","gd_besoin_c_respi",
		"f1_masse_fraiche_totale","f1_tms_pulpe","f1_masse_sec_pulpe","f1_concent_sorbitol","f1_concent_sucrose","f1_concent_glucose","f1_concent_fructose","f1_quant_sorbitol","f1_quant_sucrose","f1_quant_glucose","f1_quant_fructose","f1_surf_cracks","f1_conductance","f1_nombre_unites","f1_taux_phot_max","f1_masse_seche","f1_reserve_c","f1_besoin_c_croiss","f1_besoin_c_respi",
		"f3_masse_fraiche_totale","f3_tms_pulpe","f3_masse_sec_pulpe","f3_concent_sorbitol","f3_concent_sucrose","f3_concent_glucose","f3_concent_fructose","f3_quant_sorbitol","f3_quant_sucrose","f3_quant_glucose","f3_quant_fructose","f3_surf_cracks","f3_conductance","f3_nombre_unites","f3_taux_phot_max","f3_masse_seche","f3_reserve_c","f3_besoin_c_croiss","f3_besoin_c_respi",
		"f2_masse_fraiche_totale","f2_tms_pulpe","f2_masse_sec_pulpe","f2_concent_sorbitol","f2_concent_sucrose","f2_concent_glucose","f2_concent_fructose","f2_quant_sorbitol","f2_quant_sucrose","f2_quant_glucose","f2_quant_fructose","f2_surf_cracks","f2_conductance","f2_taux_phot_max",
		"phot_01","phot_02","phot_03","phot_04","phot_05","phot_06","phot_07","phot_08","phot_09","phot_10","phot_11","phot_12","phot_13","phot_14","phot_15","phot_16","phot_17","phot_18","phot_19","phot_20","phot_21","phot_22","phot_23","phot_24"
		)
strs_arbre = c('F_0','F_1','F_2','F_3')
strs_sphc = c('_sphc103','_sphc104','_sphc105')
strs_charge = c('','_charge_10','_charge_30','_charge_50','_charge_75','_charge_100')
d = F
d2 = F
df = F
df2 = F
nb = 0
for(str_sphc in strs_sphc){
	for(str_charge in strs_charge){
		for(str_arbre in strs_arbre){
			nb = nb + 1
			print(nb)
			name = paste(str_arbre, str_charge, str_sphc, sep='')
			data3 = read.table(paste('simulations/',name,'/',name,'_rameauxmixte.csv',sep=''),header=T,sep="\t",na.string="NULL")
			data4 = read.table(paste('simulations/',name,'/',name,'_rameaux_phot.csv',sep=''),header=T,sep="\t",na.string="NULL")
			data3 = merge(data3,data4,by=c("nom_arbre","nom_rameau","date"))
			data3$date = as.Date(data3$date)
			data3$leaf_area = data3$pf_masse_seche * 0.71 * 0.01185
			#Photosynthèse en grammes de carbone
			data3$phot = data3$leaf_area * 3600 * 1e-6 * 12 * (data3$phot_01 + data3$phot_02 + data3$phot_03 + data3$phot_04 + data3$phot_05 + data3$phot_06 + data3$phot_07 + data3$phot_08 + data3$phot_09 + data3$phot_10 + data3$phot_11 + data3$phot_12 + data3$phot_13 + data3$phot_14 + data3$phot_15 + data3$phot_16 + data3$phot_17 + data3$phot_18 + data3$phot_19 + data3$phot_20 + data3$phot_21 + data3$phot_22 + data3$phot_23 + data3$phot_24) 
			data3 = data3[,!names(data3) %in% inutiles]

			dataa = read.table( paste('simulations/',name,'/',name,'_arbre.csv',sep=''),header=T,sep="\t",na.string="NULL")
			dataa$date = as.Date(dataa$date)

			if(!d2){
				data2 = data3
				dataA = dataa
				d2 = T
			}else{
				data2 = rbind(data2, data3)
				dataA = rbind(dataA , dataa)
			}

			data_rec_s = data3[data3$date == "1998-10-15",]
			data_rec_s$sphc = str_sphc
			data_rec_s$charge = str_charge
			if(!df){
				data_rec = data_rec_s
				df = T
			}else{
				data_rec = rbind(data_rec,data_rec_s)
			}	
		}
		data2_ag = aggregate(x=data2,by = list(data2$date),FUN = somme)[,-1]
		dataA_ag = aggregate(x=dataA,by = list(dataA$date),FUN = somme)[,-1]
		data2_ag = merge(data2_ag,dataA_ag,by="date")
		data2_ag$sphc = str_sphc
		data2_ag$charge = str_charge

		if(!d){
			data = data2_ag
			d = T
		}else{
			data = rbind(data,data2_ag)
		}
		d2 = F
		
	}
}

data = data[,!names(data) %in% inutiles]
data$date = as.Date(data$date,origin="1970-01-01")

data$pf_reserve_ms = data$pf_reserve_c /( (1-0.71) * 0.4669 + 0.71 * 0.4784 )
data$f2_reserve_ms = data$f2_reserve_c / 0.4036
data$jr_reserve_ms = data$jr_reserve_c / 0.4800
data$vr_reserve_ms = data$vr_reserve_c / 0.4672
data$tl_reserve_ms = data$tl_reserve_c / 0.4707
data$vb_reserve_ms = data$vb_reserve_c / 0.4672
data$vr_reserve_ms = data$vr_reserve_c / 0.4672

data$pf_reserve_ms_p = data$pf_reserve_ms / (data$pf_masse_seche+data$pf_reserve_ms)
data$f2_reserve_ms_p = data$f2_reserve_ms / (data$f2_masse_seche+data$f2_reserve_ms)
data$jr_reserve_ms_p = data$jr_reserve_ms / (data$jr_masse_seche+data$jr_reserve_ms)
data$vr_reserve_ms_p = data$vr_reserve_ms / (data$vr_masse_seche+data$vr_reserve_ms)
data$tl_reserve_ms_p = data$tl_reserve_ms / (data$tl_masse_seche+data$tl_reserve_ms)
data$vb_reserve_ms_p = data$vb_reserve_ms / (data$vb_masse_seche+data$vb_reserve_ms)
data$vr_reserve_ms_p = data$vr_reserve_ms / (data$vr_masse_seche+data$vr_reserve_ms)

nombre_arbres = 4
for(x in names(data)){
	if(is.numeric(data[,x])){
		data[,x] = data[,x] / nombre_arbres
	}
}

data$f2_ms_moy = data$f2_masse_seche / data$f2_nombre_unites

#write.table(data,file='somme_jour.csv',sep=";")

data_rec$f2_ms_moy = data_rec$f2_masse_seche / data_rec$f2_nombre_unites



############## Histogramme fruits####################


########### Type ###############
masses_digit = read.table("fruits_98.csv",header=T,sep=";")
masses_digit$V1 = masses_digit$MS / masses_digit$n

svg("hist_rec.svg", width = 11, height = 5)
par(mfrow=c(1,2))

hist(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '',"f2_ms_moy"],xlim=c(0,60),freq=F
,breaks=0:30*2,main="Simulé",ylab="fréquence",xlab="masse sèche moyenne des fruits d'un rameau-mixte à la récolte (g)")

hist(masses_digit$V1,xlim=c(0,60),freq=F,breaks=0:30*2,
main="Observé",ylab="fréquence",xlab="masse sèche moyenne des fruits d'un rameau-mixte à la récolte (g)")
dev.off()

mean(masses_digit$V1)
sd(masses_digit$V1)

######### Stress H ############
svg("stress_hist_fruits.svg", width = 12, height = 4)

par(mfrow=c(1,3))

hist(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '',"f2_ms_moy"],xlim=c(0,45),freq=F
,breaks=0:45,main="Pas de stress",ylab="fréquence",xlab="masse sèche moyenne d'un fruit d'un rameau-mixte à la récolte (g)")

hist(data_rec[data_rec$sphc == '_sphc104' & data_rec$charge == '',"f2_ms_moy"],xlim=c(0,45),freq=F
,breaks=0:45,main="Stress modéré",ylab="fréquence",xlab="masse sèche moyenne d'un fruit d'un rameau-mixte à la récolte (g)")

hist(data_rec[data_rec$sphc == '_sphc105' & data_rec$charge == '',"f2_ms_moy"],xlim=c(0,45),freq=F
,breaks=0:45,main="Fort stress",ylab="fréquence",xlab="masse sèche moyenne d'un fruit d'un rameau-mixte à la récolte (g)")

mean(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '',"f2_ms_moy"],na.rm=T)
mean(data_rec[data_rec$sphc == '_sphc104' & data_rec$charge == '',"f2_ms_moy"],na.rm=T)
mean(data_rec[data_rec$sphc == '_sphc105' & data_rec$charge == '',"f2_ms_moy"],na.rm=T)
sd(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '',"f2_ms_moy"],na.rm=T)
sd(data_rec[data_rec$sphc == '_sphc104' & data_rec$charge == '',"f2_ms_moy"],na.rm=T)
sd(data_rec[data_rec$sphc == '_sphc105' & data_rec$charge == '',"f2_ms_moy"],na.rm=T)

dev.off()
#####################


don = data[data$sphc == "_sphc103" & data$charge == "",]

satisfaction_pf = (don$pf_masse_seche[don$date=="1998-10-15"]-don$pf_masse_seche[don$date=="1998-5-15"]) * ( (1-0.71) * (0.4669+0.0820) + 0.71 * (0.4784+0.1012) ) / sum(don$pf_besoin_c_croiss)
satisfaction_f2 = (don$f2_masse_seche[don$date=="1998-10-15"]-don$f2_masse_seche[don$date=="1998-5-15"]) * (0.4036+0.06) / sum(don$f2_besoin_c_croiss)
satisfaction_tl = (don$tl_masse_seche[don$date=="1998-10-15"]-don$tl_masse_seche[don$date=="1998-5-15"]) * (0.4707+0.0896) / sum(don$tl_besoin_c_croiss)
satisfaction_vb = (don$vb_masse_seche[don$date=="1998-10-15"]-don$vb_masse_seche[don$date=="1998-5-15"]) * (0.4672+0.0812) / sum(don$vb_besoin_c_croiss)
satisfaction_jr = (don$jr_masse_seche[don$date=="1998-10-15"]-don$jr_masse_seche[don$date=="1998-5-15"]) * (0.4800+0.0820) / sum(don$jr_besoin_c_croiss)
satisfaction_vr = (don$vr_masse_seche[don$date=="1998-10-15"]-don$vr_masse_seche[don$date=="1998-5-15"]) * (0.4672+0.0812) / sum(don$vr_besoin_c_croiss)


croissance_all = (don$pf_masse_seche[don$date=="1998-10-15"]-don$pf_masse_seche[don$date=="1998-5-15"]) * ((1-0.71) * (0.4669+0.0820) + 0.71 * (0.4784+0.1012) )+
(don$f2_masse_seche[don$date=="1998-10-15"]-don$f2_masse_seche[don$date=="1998-5-15"]) * (0.4036+0.06)+
(don$tl_masse_seche[don$date=="1998-10-15"]-don$tl_masse_seche[don$date=="1998-5-15"]) * (0.4707+0.0896)+
(don$vb_masse_seche[don$date=="1998-10-15"]-don$vb_masse_seche[don$date=="1998-5-15"]) * (0.4672+0.0812)+
(don$jr_masse_seche[don$date=="1998-10-15"]-don$jr_masse_seche[don$date=="1998-5-15"]) * (0.4800+0.0820)+
(don$vr_masse_seche[don$date=="1998-10-15"]-don$vr_masse_seche[don$date=="1998-5-15"]) * (0.4672+0.0812)
demande_all = sum(don$pf_besoin_c_croiss)+sum(don$f2_besoin_c_croiss)+sum(don$tl_besoin_c_croiss)+sum(don$vb_besoin_c_croiss)+sum(don$jr_besoin_c_croiss)+sum(don$vr_besoin_c_croiss)
croissance_all/demande_all


data$demande_tot = (data$vb_besoin_c_croiss + data$vb_besoin_c_respi
	+ data$vr_besoin_c_croiss + data$vr_besoin_c_respi
	+ data$tl_besoin_c_croiss + data$tl_besoin_c_respi
	+ data$jr_besoin_c_croiss + data$jr_besoin_c_respi
	+ data$pf_besoin_c_croiss + data$pf_besoin_c_respi
	+ data$f2_besoin_c_croiss + data$f2_besoin_c_respi)

data$ratio_offre_demande = data$phot / data$demande_tot
data$nom_arbre = data$nom_arbre.x
appercu(data,"apercu.pdf")
dev.off()

#### COurbes croissance "Type" ####
svg("croiss_type.svg", width = 9, height = 6)
par(mfrow=c(2,3))
sim_type = data[data$sphc =="_sphc103" & data$charge == "" & data$date <= "1998-10-15" & data$date > "1998-5-15",]
plot(f2_masse_seche~date,data = sim_type ,type = "l",lwd=2, xlab = "", ylab = "masse sèche (g)",
main = "A. Fruits",ylim=c(0,max(sim_type$f2_masse_seche)))
plot(pf_masse_seche~date, data=sim_type,type = "l",lwd=2, xlab = "", ylab = "masse sèche (g)",
main = "B. Pousses feuillées",ylim=c(0,max(sim_type$pf_masse_seche)))
plot(jr_masse_seche~date, data=sim_type,type = "l",lwd=2, xlab = "", ylab = "masse sèche (g)",
main = "C. Jeunes racines",ylim=c(0,max(sim_type$jr_masse_seche)))
plot(vb_masse_seche~date, data=sim_type,type = "l",lwd=2, xlab = "", ylab = "masse sèche (g)",
main = "D. Vieux bois",ylim=c(0,max(sim_type$vb_masse_seche)))
plot(tl_masse_seche~date, data=sim_type,type = "l",lwd=2, xlab = "", ylab = "masse sèche (g)",
main = "E. Bois de un an",ylim=c(0,max(sim_type$tl_masse_seche)))
plot(vr_masse_seche~date, data=sim_type,type = "l",lwd=2, xlab = "", ylab = "masse sèche (g)",
main = "F. Vieilles racines",ylim=c(0,max(sim_type$vr_masse_seche)))
dev.off()
#################

##### Diamètre rameaux #####
d = data_15_09[,c("nom_arbre","nom_rameau","tl_masse_seche","f2_nombre_unites","sphc","charge")]

a=c()
for(i in 1:length(d$nom_arbre)){
	a=c(a,paste("F_",unlist(strsplit(toString(d$nom_arbre[i]),"_"))[2],sep=""))
}

d$nom_arbre = a

d_arch = read.table("simulations/F_0_architecture.csv",sep="\t",header=T)

for(a in c("F_1","F_2","F_3")){
	d2 = read.table(paste("simulations/",a,"_architecture.csv",sep=""),sep="\t",header=T)
	d_arch = rbind(d_arch,d2)
}
d_arch = d_arch[,c("nom_arbre","nom_rameau","longueur","diametre_base","diametre_ext")]
d_arch = merge(d_arch,d,by=c("nom_arbre","nom_rameau"))
d_arch$diam = 2*(d_arch$tl_masse_seche/(4*10^-4*d_arch$longueur*pi))^0.5

d_arch_sans_courts = d_arch[d_arch$longueur>50,]
diam_digit = read.table("diam_base_uc97.txt",header=T,sep="\t",row.names = NULL)
diam_digit = diam_digit[diam_digit$Type_uc97 %in% list(2,3) & diam_digit$diam_b_uc97 != 0,]

svg("diam.svg", width = 10, height = 5)
par(mfrow=c(1,2))


hist(d_arch_sans_courts[d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "","diam"],breaks=1:30,xlab="diamètre estimé du bois de un an (mm)",ylab="nombre",
main = "A. Simulé")

hist(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites > 0 & d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "","diam"],breaks=1:30,add=TRUE,col="grey")
legend("topleft",
c("Rameaux mixtes avec fruit(s)","Rameaux mixtes sans fruits"),
fill = c("grey","white"),
box.lty = 0,
cex = 0.6
)

hist(diam_digit[diam_digit$diam_b_uc97<=40,"diam_b_uc97"],breaks=1:30,xlab="diamètre du bois de un an (mm)",ylab="nombre",main="B. Mesuré")

dev.off()

anov_diam = d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites > 0,c("diam","nom_arbre")]
anov_diam$val = "simul_avec_fruits"
a_temp = diam_digit[diam_digit$diam_b_uc97<=40,c("diam_b_uc97","Arbre")]
a_temp$val = "obs"
a_temp$diam = a_temp$diam_b_uc97
anov_diam = rbind(anov_diam[,c("diam","val")],a_temp[,c("diam","val")])
anov_diam$val = as.factor(anov_diam$val)
mod=lm(diam~val,data=anov_diam)
anova(mod)



sd(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites > 0,"diam"])
sd(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites == 0,"diam"])
sd(d_arch_sans_courts[,"diam"])


sd(diam_digit[diam_digit$diam_b_uc97<=40,c("diam_b_uc97")])

########

####### Effet stress hydrique ######

##Croissance
svg("croiss_stress.svg", width = 6, height = 6)
par(mfrow=c(2,2))

plot_stress("A. Fruits",data,"f2_masse_seche",sphc,sphc_str,c("black","black","black"),'',charge_str,type,"bottomright")
plot_stress("B Vieux bois",data,"vb_masse_seche",sphc,sphc_str,c("black","black","black"),'',charge_str,type,NA)
plot_stress("C. Bois de un an",data,"tl_masse_seche",sphc,sphc_str,c("black","black","black"),'',charge_str,type,NA)
plot_stress("D. Vieilles racines",data,"vr_masse_seche",sphc,sphc_str,c("black","black","black"),'',charge_str,type,NA)

dev.off()

##Photosynthèse
svg("phot_stress.svg", width = 6, height = 6)
plot_stress("",data,"phot_la",sphc,sphc_str,c("black","black","black"),'',charge_str,type,"bottomleft","Photosynthèse (g de carbone / jour)")
dev.off()

##Réserves
svg("res_stress.svg", width = 6, height = 6)
plot_stress("",data,"pf_reserve_ms_p",sphc,sphc_str,c("black","black","black"),'',charge_str,type,"bottomleft","carbone de réserve / carbone total")
dev.off()

##diam rameaux
svg("diam_stress.svg", width = 9, height = 3)
par(mfrow=c(1,3))
hist(d_arch_sans_courts[d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "","diam"],breaks=1:30,xlab="diamètre estimé du bois de un an (mm)",ylab="nombre",
main = "A. Pas de stress")

hist(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites > 0 & d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "","diam"],breaks=1:30,add=TRUE,col="grey")
legend("topleft",
c("Rameaux mixtes avec fruit(s)","Rameaux mixtes sans fruits"),
fill = c("grey","white"),
box.lty = 0,
cex = 0.6
)

hist(d_arch_sans_courts[d_arch_sans_courts$sphc == "_sphc104" & d_arch_sans_courts$charge == "","diam"],breaks=1:30,xlab="diamètre estimé du bois de un an (mm)",ylab="nombre",
main = "A. Stess modéré")
hist(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites > 0 & d_arch_sans_courts$sphc == "_sphc104" & d_arch_sans_courts$charge == "","diam"],breaks=1:30,add=TRUE,col="grey")

hist(d_arch_sans_courts[d_arch_sans_courts$sphc == "_sphc105" & d_arch_sans_courts$charge == "","diam"],breaks=1:30,xlab="diamètre estimé du bois de un an (mm)",ylab="nombre",
main = "A. Fort stress")
hist(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites > 0 & d_arch_sans_courts$sphc == "_sphc105" & d_arch_sans_courts$charge == "","diam"],breaks=1:30,add=TRUE,col="grey")

dev.off()
####
mean(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites > 0 & d_arch_sans_courts$sphc == "_sphc103","diam"])
mean(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites == 0 & d_arch_sans_courts$sphc == "_sphc103","diam"])
mean(d_arch_sans_courts[d_arch_sans_courts$sphc == "_sphc103","diam"])

mean(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites > 0 & d_arch_sans_courts$sphc == "_sphc104","diam"])
mean(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites == 0 & d_arch_sans_courts$sphc == "_sphc104","diam"])
mean(d_arch_sans_courts[d_arch_sans_courts$sphc == "_sphc104","diam"])

mean(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites > 0 & d_arch_sans_courts$sphc == "_sphc105","diam"])
mean(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites == 0 & d_arch_sans_courts$sphc == "_sphc105","diam"])
mean(d_arch_sans_courts[d_arch_sans_courts$sphc == "_sphc105","diam"])
###################################


############# Réserves "Type" #################
svg("reserves_type.svg", width = 9, height = 6)
par(mfrow=c(2,3))
sim_type = data[data$sphc =="_sphc103" & data$charge == "" & data$date <= "1998-10-15" & data$date > "1998-5-15",]
plot(pf_reserve_ms_p~date, data=sim_type,type = "l",lwd=2, xlab = "", ylab = "carbone de réserve / carbone total",
main = "A. Pousses feuillées",ylim=c(0,max(sim_type$pf_reserve_ms_p)))
plot(jr_reserve_ms_p~date, data=sim_type,type = "l",lwd=2, xlab = "", ylab = "carbone de réserve / carbone total",
main = "B. Jeunes racines",ylim=c(0,max(sim_type$jr_reserve_ms_p)))
plot(vb_reserve_ms_p~date, data=sim_type,type = "l",lwd=2, xlab = "", ylab = "carbone de réserve / carbone total",
main = "C. Vieux bois",ylim=c(0,max(sim_type$vb_reserve_ms_p)))
plot(tl_reserve_ms_p~date, data=sim_type,type = "l",lwd=2, xlab = "", ylab = "carbone de réserve / carbone total",
main = "D. Bois de un an",ylim=c(0,max(sim_type$tl_reserve_ms_p)))
plot(vr_reserve_ms_p~date, data=sim_type,type = "l",lwd=2, xlab = "", ylab = "carbone de réserve / carbone total",
main = "E. Vieilles racines",ylim=c(0,max(sim_type$vr_reserve_ms_p)))
dev.off()

################################################


############# Comparaison croissance / stress H ###################

c_f2_103 = data[data$date == "1998-10-15" & data$sphc == "_sphc103" & data$charge == "","f2_masse_seche"]-data[data$date == "1998-05-15" & data$sphc == "_sphc103" & data$charge == "","f2_masse_seche"]
c_f2_104 = data[data$date == "1998-10-15" & data$sphc == "_sphc104" & data$charge == "","f2_masse_seche"]-data[data$date == "1998-05-15" & data$sphc == "_sphc104" & data$charge == "","f2_masse_seche"]
c_f2_105 = data[data$date == "1998-10-15" & data$sphc == "_sphc105" & data$charge == "","f2_masse_seche"]-data[data$date == "1998-05-15" & data$sphc == "_sphc105" & data$charge == "","f2_masse_seche"]
1-c_f2_104/c_f2_103
1-c_f2_105/c_f2_103

c_tl_103 = data[data$date == "1998-10-15" & data$sphc == "_sphc103" & data$charge == "","tl_masse_seche"]-data[data$date == "1998-05-15" & data$sphc == "_sphc103" & data$charge == "","tl_masse_seche"]
c_tl_104 = data[data$date == "1998-10-15" & data$sphc == "_sphc104" & data$charge == "","tl_masse_seche"]-data[data$date == "1998-05-15" & data$sphc == "_sphc104" & data$charge == "","tl_masse_seche"]
c_tl_105 = data[data$date == "1998-10-15" & data$sphc == "_sphc105" & data$charge == "","tl_masse_seche"]-data[data$date == "1998-05-15" & data$sphc == "_sphc105" & data$charge == "","tl_masse_seche"]
1-c_tl_104/c_tl_103
1-c_tl_105/c_tl_103

c_vb_103 = data[data$date == "1998-10-15" & data$sphc == "_sphc103" & data$charge == "","vb_masse_seche"]-data[data$date == "1998-05-15" & data$sphc == "_sphc103" & data$charge == "","vb_masse_seche"]
c_vb_104 = data[data$date == "1998-10-15" & data$sphc == "_sphc104" & data$charge == "","vb_masse_seche"]-data[data$date == "1998-05-15" & data$sphc == "_sphc104" & data$charge == "","vb_masse_seche"]
c_vb_105 = data[data$date == "1998-10-15" & data$sphc == "_sphc105" & data$charge == "","vb_masse_seche"]-data[data$date == "1998-05-15" & data$sphc == "_sphc105" & data$charge == "","vb_masse_seche"]
1-c_vb_104/c_vb_103
1-c_vb_105/c_vb_103

c_vr_103 = data[data$date == "1998-10-15" & data$sphc == "_sphc103" & data$charge == "","vr_masse_seche"]-data[data$date == "1998-05-15" & data$sphc == "_sphc103" & data$charge == "","vr_masse_seche"]
c_vr_104 = data[data$date == "1998-10-15" & data$sphc == "_sphc104" & data$charge == "","vr_masse_seche"]-data[data$date == "1998-05-15" & data$sphc == "_sphc104" & data$charge == "","vr_masse_seche"]
c_vr_105 = data[data$date == "1998-10-15" & data$sphc == "_sphc105" & data$charge == "","vr_masse_seche"]-data[data$date == "1998-05-15" & data$sphc == "_sphc105" & data$charge == "","vr_masse_seche"]
1-c_vr_104/c_vr_103
1-c_vr_105/c_vr_103

################################################
plot_charge("",data,"phot",sphc,sphc_str,charge,charge_str,"bottomleft","test")



################# charge en fruits ################
##Photosynthèse
svg("phot_charge.svg", width = 6, height = 6)
plot_charge("",data,"phot",sphc,sphc_str,charge,charge_str,"bottom","Photosynthèse (g de carbone / jour)")
dev.off()


##Croissance
svg("croiss_charge.svg", width = 9, height = 6)
par(mfrow=c(2,3))

plot_charge("A. Fruits",data,"f2_masse_seche",sphc,sphc_str,charge,charge_str,NA,"masse sèche (g)")
plot_charge("B. Pousses feuillées",data,"pf_masse_seche",sphc,sphc_str,charge,charge_str,"bottom","masse sèche (g)")
plot_charge("C. Jeunes racines",data,"jr_masse_seche",sphc,sphc_str,charge,charge_str,NA,"masse sèche (g)")
plot_charge("D. Vieux bois",data,"vb_masse_seche",sphc,sphc_str,charge,charge_str,NA,"masse sèche (g)")
plot_charge("E. Bois de un an",data,"tl_masse_seche",sphc,sphc_str,charge,charge_str,NA,"masse sèche (g)")
plot_charge("F. Vieilles racines",data,"vr_masse_seche",sphc,sphc_str,charge,charge_str,NA,"masse sèche (g)")

dev.off()


##Réserves
svg("res_charge.svg", width = 6, height = 6)
plot_charge("",data,"pf_reserve_ms_p",sphc,sphc_str,charge,charge_str,"bottom","carbone de réserve / carbone total")

dev.off()

## fruits
svg("fruits_hist_charge.svg", width = 9, height = 9)

par(mfrow=c(2,2))

hist(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '_charge_10',"f2_ms_moy"],xlim=c(0,50),freq=F
,breaks=0:30*2,main="A. Taux de nouaison de 10%",ylab="fréquence",xlab="masse sèche moyenne des fruits d'un rameau-mixte à la récolte (g)")

hist(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '_charge_30',"f2_ms_moy"],xlim=c(0,50),freq=F
,breaks=0:30*2,main="B. Taux de nouaison de 30%",ylab="fréquence",xlab="masse sèche moyenne des fruits d'un rameau-mixte à la récolte (g)")

hist(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '_charge_50',"f2_ms_moy"],xlim=c(0,50),freq=F
,breaks=0:30*2,main="C. Taux de nouaison de 50%",ylab="fréquence",xlab="masse sèche moyenne des fruits d'un rameau-mixte à la récolte (g)")

hist(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '_charge_75',"f2_ms_moy"],xlim=c(0,50),freq=F
,breaks=0:30*2,main="D. Taux de nouaison de 75%",ylab="fréquence",xlab="masse sèche moyenne des fruits d'un rameau-mixte à la récolte (g)")

mean(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '_charge_10',"f2_ms_moy"],na.rm=T)
mean(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '_charge_30',"f2_ms_moy"],na.rm=T)
mean(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '_charge_50',"f2_ms_moy"],na.rm=T)
mean(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '_charge_75',"f2_ms_moy"],na.rm=T)

sd(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '_charge_10',"f2_ms_moy"],na.rm=T)
sd(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '_charge_30',"f2_ms_moy"],na.rm=T)
sd(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '_charge_50',"f2_ms_moy"],na.rm=T)
sd(data_rec[data_rec$sphc == '_sphc103' & data_rec$charge == '_charge_75',"f2_ms_moy"],na.rm=T)

dev.off()





##diam rameaux
svg("diam_charge.svg", width = 9, height = 9)

par(mfrow=c(2,2))

hist(d_arch_sans_courts[d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_10","diam"],breaks=1:35,xlab="diamètre estimé du bois de un an (mm)",ylab="nombre",
main = "A. Taux de nouaison de 10%")
hist(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites > 0 & d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_10","diam"],breaks=1:35,add=TRUE,col="grey")
legend("topleft",
c("Rameaux mixtes avec fruit(s)","Rameaux mixtes sans fruits"),
fill = c("grey","white"),
box.lty = 0,
cex = 0.6
)

hist(d_arch_sans_courts[d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_30","diam"],breaks=1:35,xlab="diamètre estimé du bois de un an (mm)",ylab="nombre",
main = "B. Taux de nouaison de 30%")
hist(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites > 0 & d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_30","diam"],breaks=1:35,add=TRUE,col="grey")

hist(d_arch_sans_courts[d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_50","diam"],breaks=1:35,xlab="diamètre estimé du bois de un an (mm)",ylab="nombre",
main = "C. Taux de nouaison de 50%")
hist(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites > 0 & d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_50","diam"],breaks=1:35,add=TRUE,col="grey")

hist(d_arch_sans_courts[d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_75","diam"],breaks=1:35,xlab="diamètre estimé du bois de un an (mm)",ylab="nombre",
main = "D. Taux de nouaison de 75%")
hist(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites > 0 & d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_75","diam"],breaks=1:35,add=TRUE,col="grey")


mean(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites == 0 & d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_10","diam"],na.rm=T)
mean(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites == 0 & d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_30","diam"],na.rm=T)
mean(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites == 0 & d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_50","diam"],na.rm=T)
mean(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites == 0 & d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_75","diam"],na.rm=T)

sd(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites == 0 & d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_10","diam"],na.rm=T)
sd(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites == 0 & d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_30","diam"],na.rm=T)
sd(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites == 0 & d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_50","diam"],na.rm=T)
sd(d_arch_sans_courts[d_arch_sans_courts$f2_nombre_unites == 0 & d_arch_sans_courts$sphc == "_sphc103" & d_arch_sans_courts$charge == "_charge_75","diam"],na.rm=T)



dev.off()



########### Comparaison avec Poll, 96 ################
###### Calcul du ratio fruit/leaf (number/kgMS) ######

data$fruit_leaf.ratio = data$f2_nombre_unites *1000 / data$pf_masse_seche

data[data$sphc == "_sphc103" & data$charge == "_charge_100" & data$date == "1998-10-15","fruit_leaf.ratio"]








png("graphv2.png")
plot(phot_la~date, data=data[data$sphc=="_sphc103" & data$charge == "" & data$date != "1998-05-15",],type = "l",ylim=c(0,6), ylab = "Phototsynthèse (g de carbone /m² / jour)",lwd = 3,cex.axis=1.4,cex.lab = 1.7)
dev.off()


