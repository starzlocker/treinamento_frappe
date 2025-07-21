media = async(frm) => {
	medirTempoValue = async(frm) => {
	  	let c = performance.now()
		const values = await frappe.db.get_value('Item', frm.docname, ["name","idx","codigo",])

		let d = performance.now()
		return d - c
	}
	
	medirTempo = async(frm) => {
	  let a = performance.now()
		const doc = await frappe.db.get_doc('Item', frm.docname)
		let b = performance.now()

		return b - a
	}
	
	somaA = 0
	somaB = 0
	for (let i = 0; i < 100; i++) {
		somaA += await medirTempo(frm)
		somaB += await medirTempoValue(frm)
	}
	
	somaA /= 100
	somaB /= 100
	
	return [somaA, somaB]
}